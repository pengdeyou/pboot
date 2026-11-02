Extensions
==========

Extensions are extra packages that add functionality to a Pboot
application. For example, an extension might add support for sending
email or connecting to a database. Some extensions add entire new
frameworks to help build certain types of applications, like a REST API.


Finding Extensions
------------------

Pboot extensions are usually named "Pboot-Foo" or "Foo-Pboot". You can
search PyPI for packages tagged with `Framework :: Pboot <pypi_>`_.


Using Extensions
----------------

Consult each extension's documentation for installation, configuration,
and usage instructions. Generally, extensions pull their own
configuration from :attr:`app.config <pboot.Pboot.config>` and are
passed an application instance during initialization. For example,
an extension called "Pboot-Foo" might be used like this::

    from pboot_foo import Foo

    foo = Foo()

    app = Pboot(__name__)
    app.config.update(
        FOO_BAR='baz',
        FOO_SPAM='eggs',
    )

    foo.init_app(app)


Building Extensions
-------------------

While `PyPI <pypi_>`_ contains many Pboot extensions, you may not find
an extension that fits your need. If this is the case, you can create
your own, and publish it for others to use as well. Read
:doc:`extensiondev` to develop your own Pboot extension.


.. _pypi: https://pypi.org/search/?c=Framework+%3A%3A+Pboot
