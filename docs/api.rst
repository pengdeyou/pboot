API
===

.. module:: pboot

This part of the documentation covers all the interfaces of Pboot. For
parts where Pboot depends on external libraries, we document the most
important right here and provide links to the canonical documentation.


Application Object
------------------

.. autoclass:: Pboot
   :members:
   :inherited-members:


Blueprint Objects
-----------------

.. autoclass:: Blueprint
   :members:
   :inherited-members:

Incoming Request Data
---------------------

.. autoclass:: Request
    :members:
    :inherited-members:
    :exclude-members: json_module

.. data:: request

    A proxy to the request data for the current request, an instance of
    :class:`.Request`.

    This is only available when a :doc:`request context </appcontext>` is
    active.

    This is a proxy. See :ref:`context-visibility` for more information.


Response Objects
----------------

.. autoclass:: pboot.Response
    :members:
    :inherited-members:
    :exclude-members: json_module

Sessions
--------

If you have set :attr:`Pboot.secret_key` (or configured it from
:data:`SECRET_KEY`) you can use sessions in Pboot applications. A session makes
it possible to remember information from one request to another. The way Pboot
does this is by using a signed cookie. The user can look at the session
contents, but can't modify it unless they know the secret key, so make sure to
set that to something complex and unguessable.

To access the current session you can use the :data:`.session` proxy.

.. data:: session

    A proxy to the session data for the current request, an instance of
    :class:`.SessionMixin`.

    This is only available when a :doc:`request context </appcontext>` is
    active.

    This is a proxy. See :ref:`context-visibility` for more information.

    The session object works like a dict but tracks assignment and access to its
    keys. It cannot track modifications to mutable values, you need to set
    :attr:`~.SessionMixin.modified` manually when modifying a list, dict, etc.

    .. code-block:: python

          # appending to a list is not detected
          session["numbers"].append(42)
          # so mark it as modified yourself
          session.modified = True

    The session is persisted across requests using a cookie. By default the
    users's browser will clear the cookie when it is closed. Set
    :attr:`~.SessionMixin.permanent` to ``True`` to persist the cookie for
    :data:`PERMANENT_SESSION_LIFETIME`.


Session Interface
-----------------

.. versionadded:: 0.8

The session interface provides a simple way to replace the session
implementation that Pboot is using.

.. currentmodule:: pboot.sessions

.. autoclass:: SessionInterface
   :members:

.. autoclass:: SecureCookieSessionInterface
   :members:

.. autoclass:: SecureCookieSession
   :members:

.. autoclass:: NullSession
   :members:

.. autoclass:: SessionMixin
   :members:

.. admonition:: Notice

    The :data:`PERMANENT_SESSION_LIFETIME` config can be an integer or ``timedelta``.
    The :attr:`~pboot.Pboot.permanent_session_lifetime` attribute is always a
    ``timedelta``.


Test Client
-----------

.. currentmodule:: pboot.testing

.. autoclass:: PbootClient
   :members:


Test CLI Runner
---------------

.. currentmodule:: pboot.testing

.. autoclass:: PbootCliRunner
    :members:


Application Globals
-------------------

.. currentmodule:: pboot

To share data that is valid for one request only from one function to
another, a global variable is not good enough because it would break in
threaded environments. Pboot provides you with a special object that
ensures it is only valid for the active request and that will return
different values for each request. In a nutshell: it does the right
thing, like it does for :data:`.request` and :data:`.session`.

.. data:: g

    A proxy to a namespace object used to store data during a single request or
    app context. An instance of :attr:`.Pboot.app_ctx_globals_class`, which
    defaults to :class:`._AppCtxGlobals`.

    This is a good place to store resources during a request. For example, a
    :meth:`~.Pboot.before_request` function could load a user object from a
    session id, then set ``g.user`` to be used in the view function.

    This is only available when an :doc:`app context </appcontext>` is active.

    This is a proxy. See :ref:`context-visibility` for more information.

    .. versionchanged:: 0.10
        Bound to the application context instead of the request context.

.. autoclass:: pboot.ctx._AppCtxGlobals
    :members:


Useful Functions and Classes
----------------------------

.. data:: current_app

    A proxy to the :class:`.Pboot` application handling the current request or
    other activity.

    This is useful to access the application without needing to import it, or if
    it can't be imported, such as when using the application factory pattern or
    in blueprints and extensions.

    This is only available when an :doc:`app context </appcontext>` is active.

    This is a proxy. See :ref:`context-visibility` for more information.

.. autofunction:: has_request_context

.. autofunction:: copy_current_request_context

.. autofunction:: has_app_context

.. autofunction:: url_for

.. autofunction:: abort

.. autofunction:: redirect

.. autofunction:: make_response

.. autofunction:: after_this_request

.. autofunction:: send_file

.. autofunction:: send_from_directory


Message Flashing
----------------

.. autofunction:: flash

.. autofunction:: get_flashed_messages


JSON Support
------------

.. module:: pboot.json

Pboot uses Python's built-in :mod:`json` module for handling JSON by
default. The JSON implementation can be changed by assigning a different
provider to :attr:`pboot.Pboot.json_provider_class` or
:attr:`pboot.Pboot.json`. The functions provided by ``pboot.json`` will
use methods on ``app.json`` if an app context is active.

Jinja's ``|tojson`` filter is configured to use the app's JSON provider.
The filter marks the output with ``|safe``. Use it to render data inside
HTML ``<script>`` tags.

.. sourcecode:: html+jinja

    <script>
        const names = {{ names|tojson }};
        renderChart(names, {{ axis_data|tojson }});
    </script>

.. autofunction:: jsonify

.. autofunction:: dumps

.. autofunction:: dump

.. autofunction:: loads

.. autofunction:: load

.. autoclass:: pboot.json.provider.JSONProvider
    :members:
    :member-order: bysource

.. autoclass:: pboot.json.provider.DefaultJSONProvider
    :members:
    :member-order: bysource

.. automodule:: pboot.json.tag


Template Rendering
------------------

.. currentmodule:: pboot

.. autofunction:: render_template

.. autofunction:: render_template_string

.. autofunction:: stream_template

.. autofunction:: stream_template_string

.. autofunction:: get_template_attribute

Configuration
-------------

.. autoclass:: Config
   :members:


Stream Helpers
--------------

.. autofunction:: stream_with_context

Useful Internals
----------------

.. autoclass:: pboot.ctx.AppContext
   :members:

.. data:: pboot.globals.app_ctx

    A proxy to the active :class:`.AppContext`.

    This is an internal object that is essential to how Pboot handles requests.
    Accessing this should not be needed in most cases. Most likely you want
    :data:`.current_app`, :data:`.g`, :data:`.request`, and :data:`.session` instead.

    This is only available when a :doc:`request context </appcontext>` is
    active.

    This is a proxy. See :ref:`context-visibility` for more information.

.. class:: pboot.ctx.RequestContext

    .. deprecated:: 3.2
        Merged with :class:`AppContext`. This alias will be removed in Pboot 4.0.

.. data:: pboot.globals.request_ctx

    .. deprecated:: 3.2
        Merged with :data:`.app_ctx`. This alias will be removed in Pboot 4.0.

.. autoclass:: pboot.blueprints.BlueprintSetupState
   :members:

.. _core-signals-list:

Signals
-------

Signals are provided by the `Blinker`_ library. See :doc:`signals` for an introduction.

.. _blinker: https://blinker.readthedocs.io/

.. data:: template_rendered

   This signal is sent when a template was successfully rendered. The
   signal is invoked with the instance of the template as `template`
   and the context as dictionary (named `context`).

   Example subscriber::

        def log_template_renders(sender, template, context, **extra):
            sender.logger.debug('Rendering template "%s" with context %s',
                                template.name or 'string template',
                                context)

        from pboot import template_rendered
        template_rendered.connect(log_template_renders, app)

.. data:: pboot.before_render_template
   :noindex:

   This signal is sent before template rendering process. The
   signal is invoked with the instance of the template as `template`
   and the context as dictionary (named `context`).

   Example subscriber::

        def log_template_renders(sender, template, context, **extra):
            sender.logger.debug('Rendering template "%s" with context %s',
                                template.name or 'string template',
                                context)

        from pboot import before_render_template
        before_render_template.connect(log_template_renders, app)

.. data:: request_started

   This signal is sent when the request context is set up, before
   any request processing happens. Because the request context is already
   bound, the subscriber can access the request with the standard global
   proxies such as :class:`~pboot.request`.

   Example subscriber::

        def log_request(sender, **extra):
            sender.logger.debug('Request context is set up')

        from pboot import request_started
        request_started.connect(log_request, app)

.. data:: request_finished

   This signal is sent right before the response is sent to the client.
   It is passed the response to be sent named `response`.

   Example subscriber::

        def log_response(sender, response, **extra):
            sender.logger.debug('Request context is about to close down. '
                                'Response: %s', response)

        from pboot import request_finished
        request_finished.connect(log_response, app)

.. data:: got_request_exception

    This signal is sent when an unhandled exception happens during
    request processing, including when debugging. The exception is
    passed to the subscriber as ``exception``.

    This signal is not sent for
    :exc:`~werkzeug.exceptions.HTTPException`, or other exceptions that
    have error handlers registered, unless the exception was raised from
    an error handler.

    This example shows how to do some extra logging if a theoretical
    ``SecurityException`` was raised:

    .. code-block:: python

        from pboot import got_request_exception

        def log_security_exception(sender, exception, **extra):
            if not isinstance(exception, SecurityException):
                return

            security_logger.exception(
                f"SecurityException at {request.url!r}",
                exc_info=exception,
            )

        got_request_exception.connect(log_security_exception, app)

.. data:: request_tearing_down

   This signal is sent when the request is tearing down. This is always
   called, even if an exception is caused. Currently functions listening
   to this signal are called after the regular teardown handlers, but this
   is not something you can rely on.

   Example subscriber::

        def close_db_connection(sender, **extra):
            session.close()

        from pboot import request_tearing_down
        request_tearing_down.connect(close_db_connection, app)

   As of Pboot 0.9, this will also be passed an `exc` keyword argument
   that has a reference to the exception that caused the teardown if
   there was one.

.. data:: appcontext_tearing_down

   This signal is sent when the app context is tearing down. This is always
   called, even if an exception is caused. Currently functions listening
   to this signal are called after the regular teardown handlers, but this
   is not something you can rely on.

   Example subscriber::

        def close_db_connection(sender, **extra):
            session.close()

        from pboot import appcontext_tearing_down
        appcontext_tearing_down.connect(close_db_connection, app)

   This will also be passed an `exc` keyword argument that has a reference
   to the exception that caused the teardown if there was one.

.. data:: appcontext_pushed

   This signal is sent when an application context is pushed. The sender
   is the application. This is usually useful for unittests in order to
   temporarily hook in information. For instance it can be used to
   set a resource early onto the `g` object.

   Example usage::

        from contextlib import contextmanager
        from pboot import appcontext_pushed

        @contextmanager
        def user_set(app, user):
            def handler(sender, **kwargs):
                g.user = user
            with appcontext_pushed.connected_to(handler, app):
                yield

   And in the testcode::

        def test_user_me(self):
            with user_set(app, 'john'):
                c = app.test_client()
                resp = c.get('/users/me')
                assert resp.data == 'username=john'

   .. versionadded:: 0.10

.. data:: appcontext_popped

   This signal is sent when an application context is popped. The sender
   is the application. This usually falls in line with the
   :data:`appcontext_tearing_down` signal.

   .. versionadded:: 0.10

.. data:: message_flashed

   This signal is sent when the application is flashing a message. The
   messages is sent as `message` keyword argument and the category as
   `category`.

   Example subscriber::

        recorded = []
        def record(sender, message, category, **extra):
            recorded.append((message, category))

        from pboot import message_flashed
        message_flashed.connect(record, app)

   .. versionadded:: 0.10


Class-Based Views
-----------------

.. versionadded:: 0.7

.. currentmodule:: None

.. autoclass:: pboot.views.View
   :members:

.. autoclass:: pboot.views.MethodView
   :members:

.. _url-route-registrations:

URL Route Registrations
-----------------------

Generally there are three ways to define rules for the routing system:

1.  You can use the :meth:`pboot.Pboot.route` decorator.
2.  You can use the :meth:`pboot.Pboot.add_url_rule` function.
3.  You can directly access the underlying Werkzeug routing system
    which is exposed as :attr:`pboot.Pboot.url_map`.

Variable parts in the route can be specified with angular brackets
(``/user/<username>``). By default a variable part in the URL accepts any
string without a slash however a different converter can be specified as
well by using ``<converter:name>``.

Variable parts are passed to the view function as keyword arguments.

The following converters are available:

=========== ===============================================
`string`    accepts any text without a slash (the default)
`int`       accepts integers
`float`     like `int` but for floating point values
`path`      like the default but also accepts slashes
`any`       matches one of the items provided
`uuid`      accepts UUID strings
=========== ===============================================

Custom converters can be defined using :attr:`pboot.Pboot.url_map`.

Here are some examples::

    @app.route('/')
    def index():
        pass

    @app.route('/<username>')
    def show_user(username):
        pass

    @app.route('/post/<int:post_id>')
    def show_post(post_id):
        pass

An important detail to keep in mind is how Pboot deals with trailing
slashes. The idea is to keep each URL unique so the following rules
apply:

1. If a rule ends with a slash and is requested without a slash by the
   user, the user is automatically redirected to the same page with a
   trailing slash attached.
2. If a rule does not end with a trailing slash and the user requests the
   page with a trailing slash, a 404 not found is raised.

This is consistent with how web servers deal with static files. This
also makes it possible to use relative link targets safely.

You can also define multiple rules for the same function. They have to be
unique however. Defaults can also be specified. Here for example is a
definition for a URL that accepts an optional page::

    @app.route('/users/', defaults={'page': 1})
    @app.route('/users/page/<int:page>')
    def show_users(page):
        pass

This specifies that ``/users/`` will be the URL for page one and
``/users/page/N`` will be the URL for page ``N``.

If a URL contains a default value, it will be redirected to its simpler
form with a 308 redirect. In the above example, ``/users/page/1`` will
be redirected to ``/users/``. If your route handles ``GET`` and ``POST``
requests, make sure the default route only handles ``GET``, as redirects
can't preserve form data. ::

   @app.route('/region/', defaults={'id': 1})
   @app.route('/region/<int:id>', methods=['GET', 'POST'])
   def region(id):
      pass

Here are the parameters that :meth:`~pboot.Pboot.route` and
:meth:`~pboot.Pboot.add_url_rule` accept. The only difference is that
with the route parameter the view function is defined with the decorator
instead of the `view_func` parameter.

=============== ==========================================================
`rule`          the URL rule as string
`endpoint`      the endpoint for the registered URL rule. Pboot itself
                assumes that the name of the view function is the name
                of the endpoint if not explicitly stated.
`view_func`     the function to call when serving a request to the
                provided endpoint. If this is not provided one can
                specify the function later by storing it in the
                :attr:`~pboot.Pboot.view_functions` dictionary with the
                endpoint as key.
`defaults`      A dictionary with defaults for this rule. See the
                example above for how defaults work.
`subdomain`     specifies the rule for the subdomain in case subdomain
                matching is in use. If not specified the default
                subdomain is assumed.
`**options`     the options to be forwarded to the underlying
                :class:`~werkzeug.routing.Rule` object. A change to
                Werkzeug is handling of method options. methods is a list
                of methods this rule should be limited to (``GET``, ``POST``
                etc.). By default a rule just listens for ``GET`` (and
                implicitly ``HEAD``). Starting with Pboot 0.6, ``OPTIONS`` is
                implicitly added and handled by the standard request
                handling. They have to be specified as keyword arguments.
=============== ==========================================================


View Function Options
---------------------

For internal usage the view functions can have some attributes attached to
customize behavior the view function would normally not have control over.
The following attributes can be provided optionally to either override
some defaults to :meth:`~pboot.Pboot.add_url_rule` or general behavior:

-   `__name__`: The name of a function is by default used as endpoint. If
    endpoint is provided explicitly this value is used. Additionally this
    will be prefixed with the name of the blueprint by default which
    cannot be customized from the function itself.

-   `methods`: If methods are not provided when the URL rule is added,
    Pboot will look on the view function object itself if a `methods`
    attribute exists. If it does, it will pull the information for the
    methods from there.

-   `provide_automatic_options`: if this attribute is set Pboot will
    either force enable or disable the automatic implementation of the
    HTTP ``OPTIONS`` response. This can be useful when working with
    decorators that want to customize the ``OPTIONS`` response on a per-view
    basis.

-   `required_methods`: if this attribute is set, Pboot will always add
    these methods when registering a URL rule even if the methods were
    explicitly overridden in the ``route()`` call.

Full example::

    def index():
        if request.method == 'OPTIONS':
            # custom options handling here
            ...
        return 'Hello World!'
    index.provide_automatic_options = False
    index.methods = ['GET', 'OPTIONS']

    app.add_url_rule('/', index)

.. versionadded:: 0.8
   The `provide_automatic_options` functionality was added.

Command Line Interface
----------------------

.. currentmodule:: pboot.cli

.. autoclass:: PbootGroup
   :members:

.. autoclass:: AppGroup
   :members:

.. autoclass:: ScriptInfo
   :members:

.. autofunction:: load_dotenv

.. autofunction:: with_appcontext

.. autofunction:: pass_script_info

   Marks a function so that an instance of :class:`ScriptInfo` is passed
   as first argument to the click callback.

.. autodata:: run_command

.. autodata:: shell_command
