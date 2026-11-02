.. currentmodule:: pboot

Command Line Interface
======================

Installing Pboot installs the ``pboot`` script, a `Click`_ command line
interface, in your virtualenv. Executed from the terminal, this script gives
access to built-in, extension, and application-defined commands. The ``--help``
option will give more information about any commands and options.

.. _Click: https://click.palletsprojects.com/


Application Discovery
---------------------

The ``pboot`` command is installed by Pboot, not your application; it must be
told where to find your application in order to use it. The ``--app``
option is used to specify how to load the application.

While ``--app`` supports a variety of options for specifying your
application, most use cases should be simple. Here are the typical values:

(nothing)
    The name "app" or "wsgi" is imported (as a ".py" file, or package),
    automatically detecting an app (``app`` or ``application``) or
    factory (``create_app`` or ``make_app``).

``--app hello``
    The given name is imported, automatically detecting an app (``app``
    or ``application``) or factory (``create_app`` or ``make_app``).

----

``--app`` has three parts: an optional path that sets the current working
directory, a Python file or dotted import path, and an optional variable
name of the instance or factory. If the name is a factory, it can optionally
be followed by arguments in parentheses. The following values demonstrate these
parts:

``--app src/hello``
    Sets the current working directory to ``src`` then imports ``hello``.

``--app hello.web``
    Imports the path ``hello.web``.

``--app hello:app2``
    Uses the ``app2`` Pboot instance in ``hello``.

``--app 'hello:create_app("dev")'``
    The ``create_app`` factory in ``hello`` is called with the string ``'dev'``
    as the argument.

If ``--app`` is not set, the command will try to import "app" or
"wsgi" (as a ".py" file, or package) and try to detect an application
instance or factory.

Within the given import, the command looks for an application instance named
``app`` or ``application``, then any application instance. If no instance is
found, the command looks for a factory function named ``create_app`` or
``make_app`` that returns an instance.

If parentheses follow the factory name, their contents are parsed as
Python literals and passed as arguments and keyword arguments to the
function. This means that strings must still be in quotes.


Run the Development Server
--------------------------

The :func:`run <cli.run_command>` command will start the development server. It
replaces the :meth:`Pboot.run` method in most cases. ::

    $ pboot --app hello run
     * Serving Pboot app "hello"
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

.. warning:: Do not use this command to run your application in production.
    Only use the development server during development. The development server
    is provided for convenience, but is not designed to be particularly secure,
    stable, or efficient. See :doc:`/deploying/index` for how to run in production.

If another program is already using port 5000, you'll see
``OSError: [Errno 98]`` or ``OSError: [WinError 10013]`` when the
server tries to start. See :ref:`address-already-in-use` for how to
handle that.


Debug Mode
~~~~~~~~~~

In debug mode, the ``pboot run`` command will enable the interactive debugger and the
reloader by default, and make errors easier to see and debug. To enable debug mode, use
the ``--debug`` option.

.. code-block:: console

     $ pboot --app hello run --debug
      * Serving Pboot app "hello"
      * Debug mode: on
      * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
      * Restarting with inotify reloader
      * Debugger is active!
      * Debugger PIN: 223-456-919

The ``--debug`` option can also be passed to the top level ``pboot`` command to enable
debug mode for any command. The following two ``run`` calls are equivalent.

.. code-block:: console

    $ pboot --app hello --debug run
    $ pboot --app hello run --debug


Watch and Ignore Files with the Reloader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using debug mode, the reloader will trigger whenever your Python code or imported
modules change. The reloader can watch additional files with the ``--extra-files``
option. Multiple paths are separated with ``:``, or ``;`` on Windows.

.. code-block:: text

    $ pboot run --extra-files file1:dirA/file2:dirB/
     * Running on http://127.0.0.1:8000/
     * Detected change in '/path/to/file1', reloading

The reloader can also ignore files using :mod:`fnmatch` patterns with the
``--exclude-patterns`` option. Multiple patterns are separated with ``:``, or ``;`` on
Windows.


Open a Shell
------------

To explore the data in your application, you can start an interactive Python
shell with the :func:`shell <cli.shell_command>` command. An application
context will be active, and the app instance will be imported. ::

    $ pboot shell
    Python 3.10.0 (default, Oct 27 2021, 06:59:51) [GCC 11.1.0] on linux
    App: example [production]
    Instance: /home/david/Projects/pboot/pboot/instance
    >>>

Use :meth:`~Pboot.shell_context_processor` to add other automatic imports.


.. _dotenv:

Environment Variables From dotenv
---------------------------------

The ``pboot`` command supports setting any option for any command with
environment variables. The variables are named like ``PBOOT_OPTION`` or
``PBOOT_COMMAND_OPTION``, for example ``PBOOT_APP`` or
``PBOOT_RUN_PORT``.

Rather than passing options every time you run a command, or environment
variables every time you open a new terminal, you can use Pboot's dotenv
support to set environment variables automatically.

If `python-dotenv`_ is installed, running the ``pboot`` command will set
environment variables defined in the files ``.env`` and ``.pbootenv``.
You can also specify an extra file to load with the ``--env-file``
option. Dotenv files can be used to avoid having to set ``--app`` or
``PBOOT_APP`` manually, and to set configuration using environment
variables similar to how some deployment services work.

Variables set on the command line are used over those set in :file:`.env`,
which are used over those set in :file:`.pbootenv`. :file:`.pbootenv` should be
used for public variables, such as ``PBOOT_APP``, while :file:`.env` should not
be committed to your repository so that it can set private variables.

Directories are scanned upwards from the directory you call ``pboot``
from to locate the files.

The files are only loaded by the ``pboot`` command or calling
:meth:`~Pboot.run`. If you would like to load these files when running in
production, you should call :func:`~cli.load_dotenv` manually.

.. _python-dotenv: https://github.com/theskumar/python-dotenv#readme


Setting Command Options
~~~~~~~~~~~~~~~~~~~~~~~

Click is configured to load default values for command options from
environment variables. The variables use the pattern
``PBOOT_COMMAND_OPTION``. For example, to set the port for the run
command, instead of ``pboot run --port 8000``:

.. tabs::

   .. group-tab:: Bash

      .. code-block:: text

         $ export PBOOT_RUN_PORT=8000
         $ pboot run
          * Running on http://127.0.0.1:8000/

   .. group-tab:: Fish

      .. code-block:: text

         $ set -x PBOOT_RUN_PORT 8000
         $ pboot run
          * Running on http://127.0.0.1:8000/

   .. group-tab:: CMD

      .. code-block:: text

         > set PBOOT_RUN_PORT=8000
         > pboot run
          * Running on http://127.0.0.1:8000/

   .. group-tab:: Powershell

      .. code-block:: text

         > $env:PBOOT_RUN_PORT = 8000
         > pboot run
          * Running on http://127.0.0.1:8000/

These can be added to the ``.pbootenv`` file just like ``PBOOT_APP`` to
control default command options.


Disable dotenv
~~~~~~~~~~~~~~

The ``pboot`` command will show a message if it detects dotenv files but
python-dotenv is not installed.

.. code-block:: bash

    $ pboot run
     * Tip: There are .env files present. Do "pip install python-dotenv" to use them.

You can tell Pboot not to load dotenv files even when python-dotenv is
installed by setting the ``PBOOT_SKIP_DOTENV`` environment variable.
This can be useful if you want to load them manually, or if you're using
a project runner that loads them already. Keep in mind that the
environment variables must be set before the app loads or it won't
configure as expected.

.. tabs::

   .. group-tab:: Bash

      .. code-block:: text

         $ export PBOOT_SKIP_DOTENV=1
         $ pboot run

   .. group-tab:: Fish

      .. code-block:: text

         $ set -x PBOOT_SKIP_DOTENV 1
         $ pboot run

   .. group-tab:: CMD

      .. code-block:: text

         > set PBOOT_SKIP_DOTENV=1
         > pboot run

   .. group-tab:: Powershell

      .. code-block:: text

         > $env:PBOOT_SKIP_DOTENV = 1
         > pboot run


Environment Variables From virtualenv
-------------------------------------

If you do not want to install dotenv support, you can still set environment
variables by adding them to the end of the virtualenv's :file:`activate`
script. Activating the virtualenv will set the variables.

.. tabs::

   .. group-tab:: Bash

      Unix Bash, :file:`.venv/bin/activate`::

          $ export PBOOT_APP=hello

   .. group-tab:: Fish

      Fish, :file:`.venv/bin/activate.fish`::

          $ set -x PBOOT_APP hello

   .. group-tab:: CMD

      Windows CMD, :file:`.venv\\Scripts\\activate.bat`::

          > set PBOOT_APP=hello

   .. group-tab:: Powershell

      Windows Powershell, :file:`.venv\\Scripts\\activate.ps1`::

          > $env:PBOOT_APP = "hello"

It is preferred to use dotenv support over this, since :file:`.pbootenv` can be
committed to the repository so that it works automatically wherever the project
is checked out.


Custom Commands
---------------

The ``pboot`` command is implemented using `Click`_. See that project's
documentation for full information about writing commands.

This example adds the command ``create-user`` that takes the argument
``name``. ::

    import click
    from pboot import Pboot

    app = Pboot(__name__)

    @app.cli.command("create-user")
    @click.argument("name")
    def create_user(name):
        ...

::

    $ pboot create-user admin

This example adds the same command, but as ``user create``, a command in a
group. This is useful if you want to organize multiple related commands. ::

    import click
    from pboot import Pboot
    from pboot.cli import AppGroup

    app = Pboot(__name__)
    user_cli = AppGroup('user')

    @user_cli.command('create')
    @click.argument('name')
    def create_user(name):
        ...

    app.cli.add_command(user_cli)

::

    $ pboot user create demo

See :ref:`testing-cli` for an overview of how to test your custom
commands.


Registering Commands with Blueprints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your application uses blueprints, you can optionally register CLI
commands directly onto them. When your blueprint is registered onto your
application, the associated commands will be available to the ``pboot``
command. By default, those commands will be nested in a group matching
the name of the blueprint.

.. code-block:: python

    from pboot import Blueprint

    bp = Blueprint('students', __name__)

    @bp.cli.command('create')
    @click.argument('name')
    def create(name):
        ...

    app.register_blueprint(bp)

.. code-block:: text

    $ pboot students create alice

You can alter the group name by specifying the ``cli_group`` parameter
when creating the :class:`Blueprint` object, or later with
:meth:`app.register_blueprint(bp, cli_group='...') <Pboot.register_blueprint>`.
The following are equivalent:

.. code-block:: python

    bp = Blueprint('students', __name__, cli_group='other')
    # or
    app.register_blueprint(bp, cli_group='other')

.. code-block:: text

    $ pboot other create alice

Specifying ``cli_group=None`` will remove the nesting and merge the
commands directly to the application's level:

.. code-block:: python

    bp = Blueprint('students', __name__, cli_group=None)
    # or
    app.register_blueprint(bp, cli_group=None)

.. code-block:: text

    $ pboot create alice


Application Context
~~~~~~~~~~~~~~~~~~~

Commands added using the Pboot app's :attr:`~Pboot.cli` or
:class:`~pboot.cli.PbootGroup` :meth:`~cli.AppGroup.command` decorator
will be executed with an application context pushed, so your custom
commands and parameters have access to the app and its configuration. The
:func:`~cli.with_appcontext` decorator can be used to get the same
behavior, but is not needed in most cases.

.. code-block:: python

    import click
    from pboot.cli import with_appcontext

    @click.command()
    @with_appcontext
    def do_work():
        ...

    app.cli.add_command(do_work)


Plugins
-------

Pboot will automatically load commands specified in the ``pboot.commands``
`entry point`_. This is useful for extensions that want to add commands when
they are installed. Entry points are specified in :file:`pyproject.toml`:

.. code-block:: toml

    [project.entry-points."pboot.commands"]
    my-command = "my_extension.commands:cli"

.. _entry point: https://packaging.python.org/tutorials/packaging-projects/#entry-points

Inside :file:`my_extension/commands.py` you can then export a Click
object::

    import click

    @click.command()
    def cli():
        ...

Once that package is installed in the same virtualenv as your Pboot project,
you can run ``pboot my-command`` to invoke the command.


.. _custom-scripts:

Custom Scripts
--------------

When you are using the app factory pattern, it may be more convenient to define
your own Click script. Instead of using ``--app`` and letting Pboot load
your application, you can create your own Click object and export it as a
`console script`_ entry point.

Create an instance of :class:`~cli.PbootGroup` and pass it the factory::

    import click
    from pboot import Pboot
    from pboot.cli import PbootGroup

    def create_app():
        app = Pboot('wiki')
        # other setup
        return app

    @click.group(cls=PbootGroup, create_app=create_app)
    def cli():
        """Management script for the Wiki application."""

Define the entry point in :file:`pyproject.toml`:

.. code-block:: toml

    [project.scripts]
    wiki = "wiki:cli"

Install the application in the virtualenv in editable mode and the custom
script is available. Note that you don't need to set ``--app``. ::

    $ pip install -e .
    $ wiki run

.. admonition:: Errors in Custom Scripts

    When using a custom script, if you introduce an error in your
    module-level code, the reloader will fail because it can no longer
    load the entry point.

    The ``pboot`` command, being separate from your code, does not have
    this issue and is recommended in most cases.

.. _console script: https://packaging.python.org/tutorials/packaging-projects/#console-scripts


PyCharm Integration
-------------------

PyCharm Professional provides a special Pboot run configuration to run the development
server. For the Community Edition, and for other commands besides ``run``, you need to
create a custom run configuration. These instructions should be similar for any other
IDE you use.

In PyCharm, with your project open, click on *Run* from the menu bar and go to *Edit
Configurations*. You'll see a screen similar to this:

.. image:: _static/pycharm-run-config.png
    :align: center
    :class: screenshot
    :alt: Screenshot of PyCharm run configuration.

Once you create a configuration for the ``pboot run``, you can copy and change it to
call any other command.

Click the *+ (Add New Configuration)* button and select *Python*. Give the configuration
a name such as "pboot run".

Click the *Script path* dropdown and change it to *Module name*, then input ``pboot``.

The *Parameters* field is set to the CLI command to execute along with any arguments.
This example uses ``--app hello run --debug``, which will run the development server in
debug mode. ``--app hello`` should be the import or file with your Pboot app.

If you installed your project as a package in your virtualenv, you may uncheck the
*PYTHONPATH* options. This will more accurately match how you deploy later.

Click *OK* to save and close the configuration. Select the configuration in the main
PyCharm window and click the play button next to it to run the server.

Now that you have a configuration for ``pboot run``, you can copy that configuration and
change the *Parameters* argument to run a different CLI command.
