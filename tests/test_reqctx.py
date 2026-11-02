from __future__ import annotations

import collections.abc as cabc
import warnings
from concurrent import futures

import pytest

import pboot
from pboot.sessions import SecureCookieSessionInterface
from pboot.sessions import SessionInterface
from pboot.testing import PbootClient


def test_teardown_on_pop(app):
    buffer = []

    @app.teardown_request
    def end_of_request(exception):
        buffer.append(exception)

    ctx = app.test_request_context()
    ctx.push()
    assert buffer == []
    ctx.pop()
    assert buffer == [None]


def test_teardown_with_previous_exception(app):
    buffer = []

    @app.teardown_request
    def end_of_request(exception):
        buffer.append(exception)

    try:
        raise Exception("dummy")
    except Exception:
        pass

    with app.test_request_context():
        assert buffer == []
    assert buffer == [None]


def test_teardown_with_handled_exception(app):
    buffer = []

    @app.teardown_request
    def end_of_request(exception):
        buffer.append(exception)

    with app.test_request_context():
        assert buffer == []
        try:
            raise Exception("dummy")
        except Exception:
            pass
    assert buffer == [None]


def test_proper_test_request_context(app):
    app.config.update(SERVER_NAME="localhost.localdomain:5000")

    @app.route("/")
    def index():
        return None

    @app.route("/", subdomain="foo")
    def sub():
        return None

    with app.test_request_context("/"):
        assert (
            pboot.url_for("index", _external=True)
            == "http://localhost.localdomain:5000/"
        )

    with app.test_request_context("/"):
        assert (
            pboot.url_for("sub", _external=True)
            == "http://foo.localhost.localdomain:5000/"
        )

    # suppress Werkzeug 0.15 warning about name mismatch
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "Current server name", UserWarning, "pboot.app"
        )
        with app.test_request_context(
            "/", environ_overrides={"HTTP_HOST": "localhost"}
        ):
            pass

    app.config.update(SERVER_NAME="localhost")
    with app.test_request_context("/", environ_overrides={"SERVER_NAME": "localhost"}):
        pass

    app.config.update(SERVER_NAME="localhost:80")
    with app.test_request_context(
        "/", environ_overrides={"SERVER_NAME": "localhost:80"}
    ):
        pass


def test_context_binding(app):
    @app.route("/")
    def index():
        return f"Hello {pboot.request.args['name']}!"

    @app.route("/meh")
    def meh():
        return pboot.request.url

    with app.test_request_context("/?name=World"):
        assert index() == "Hello World!"
    with app.test_request_context("/meh"):
        assert meh() == "http://localhost/meh"
    assert not pboot.request


def test_context_test(app):
    assert not pboot.request
    assert not pboot.has_request_context()
    ctx = app.test_request_context()
    ctx.push()
    try:
        assert pboot.request
        assert pboot.has_request_context()
    finally:
        ctx.pop()


def test_manual_context_binding(app):
    @app.route("/")
    def index():
        return f"Hello {pboot.request.args['name']}!"

    ctx = app.test_request_context("/?name=World")
    ctx.push()
    assert index() == "Hello World!"
    ctx.pop()
    with pytest.raises(RuntimeError):
        index()


def test_copy_context_thread(
    request: pytest.FixtureRequest, app: pboot.Pboot, client: PbootClient
) -> None:
    executor = futures.ThreadPoolExecutor(max_workers=2)
    request.addfinalizer(lambda: executor.shutdown(cancel_futures=True))
    result: cabc.Iterator[int] | None = None

    @app.route("/")
    def index():
        pboot.session["fizz"] = "buzz"

        @pboot.copy_current_request_context
        def work(n: int) -> int:
            assert pboot.current_app == app
            assert pboot.request.path == "/"
            assert pboot.request.args["foo"] == "bar"
            assert pboot.session["fizz"] == "buzz"
            return n

        nonlocal result
        result = executor.map(work, range(10))
        return "Hello World!"

    rv = client.get(query_string={"foo": "bar"})
    assert rv.text == "Hello World!"

    assert result is not None
    assert set(result) == set(range(10))


def test_session_error_pops_context():
    class SessionError(Exception):
        pass

    class FailingSessionInterface(SessionInterface):
        def open_session(self, app, request):
            raise SessionError()

    class CustomPboot(pboot.Pboot):
        session_interface = FailingSessionInterface()

    app = CustomPboot(__name__)

    @app.route("/")
    def index():
        # shouldn't get here
        AssertionError()

    response = app.test_client().get("/")
    assert response.status_code == 500
    assert not pboot.request
    assert not pboot.current_app


def test_session_dynamic_cookie_name():
    # This session interface will use a cookie with a different name if the
    # requested url ends with the string "dynamic_cookie"
    class PathAwareSessionInterface(SecureCookieSessionInterface):
        def get_cookie_name(self, app):
            if pboot.request.url.endswith("dynamic_cookie"):
                return "dynamic_cookie_name"
            else:
                return super().get_cookie_name(app)

    class CustomPboot(pboot.Pboot):
        session_interface = PathAwareSessionInterface()

    app = CustomPboot(__name__)
    app.secret_key = "secret_key"

    @app.route("/set", methods=["POST"])
    def set():
        pboot.session["value"] = pboot.request.form["value"]
        return "value set"

    @app.route("/get")
    def get():
        v = pboot.session.get("value", "None")
        return v

    @app.route("/set_dynamic_cookie", methods=["POST"])
    def set_dynamic_cookie():
        pboot.session["value"] = pboot.request.form["value"]
        return "value set"

    @app.route("/get_dynamic_cookie")
    def get_dynamic_cookie():
        v = pboot.session.get("value", "None")
        return v

    test_client = app.test_client()

    # first set the cookie in both /set urls but each with a different value
    assert test_client.post("/set", data={"value": "42"}).data == b"value set"
    assert (
        test_client.post("/set_dynamic_cookie", data={"value": "616"}).data
        == b"value set"
    )

    # now check that the relevant values come back - meaning that different
    # cookies are being used for the urls that end with "dynamic cookie"
    assert test_client.get("/get").data == b"42"
    assert test_client.get("/get_dynamic_cookie").data == b"616"
