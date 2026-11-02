.. rst-class:: hide-header

Welcome to Pboot
================

.. image:: _static/pboot-name.svg
    :align: center
    :height: 200px

Welcome to Pboot's documentation. Pboot is a lightweight WSGI web application framework.
It is designed to make getting started quick and easy, with the ability to scale up to
complex applications.

Get started with :doc:`installation`
and then get an overview with the :doc:`quickstart`. There is also a
more detailed :doc:`tutorial/index` that shows how to create a small but
complete application with Pboot. Common patterns are described in the
:doc:`patterns/index` section. The rest of the docs describe each
component of Pboot in detail, with a full reference in the :doc:`api`
section.

Pboot depends on the `Werkzeug`_ WSGI toolkit, the `Jinja`_ template engine, and the
`Click`_ CLI toolkit. Be sure to check their documentation as well as Pboot's when
looking for information.

.. _Werkzeug: https://werkzeug.palletsprojects.com
.. _Jinja: https://jinja.palletsprojects.com
.. _Click: https://click.palletsprojects.com


User's Guide
------------

Pboot provides configuration and conventions, with sensible defaults, to get started.
This section of the documentation explains the different parts of the Pboot framework
and how they can be used, customized, and extended. Beyond Pboot itself, look for
community-maintained extensions to add even more functionality.

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   tutorial/index
   templating
   testing
   errorhandling
   debugging
   logging
   config
   signals
   views
   lifecycle
   appcontext
   blueprints
   extensions
   cli
   server
   shell
   patterns/index
   web-security
   deploying/index
   gevent
   async-await


API Reference
-------------

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api


Additional Notes
----------------

.. toctree::
   :maxdepth: 2

   design
   extensiondev
   contributing
   license
   changes
