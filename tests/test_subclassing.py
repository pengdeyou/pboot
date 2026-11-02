from io import StringIO

import pboot


def test_suppressed_exception_logging():
    class SuppressedPboot(pboot.Pboot):
        def log_exception(self, ctx, exc_info):
            pass

    out = StringIO()
    app = SuppressedPboot(__name__)

    @app.route("/")
    def index():
        raise Exception("test")

    rv = app.test_client().get("/", errors_stream=out)
    assert rv.status_code == 500
    assert b"Internal Server Error" in rv.data
    assert not out.getvalue()
