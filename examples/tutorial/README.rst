Pbootr
======

The basic blog app built in the Pboot `tutorial`_.

.. _tutorial: https://gitee.com/pboot-org/pboot/tree/main/examples/tutorial


Install
-------

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the main branch. ::

    # clone the repository
    $ git clone https://gitee.com/pboot-org/pboot
    $ cd pboot
    # checkout the correct version
    $ git tag  # shows the tagged versions
    $ git checkout latest-tag-found-above
    $ cd examples/tutorial

Create a virtualenv and activate it::

    $ python3 -m venv .venv
    $ . .venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv .venv
    $ .venv\Scripts\activate.bat

Install Pbootr::

    $ pip install -e .

Or if you are using the main branch, install Pboot from source before
installing Pbootr::

    $ pip install -e ../..
    $ pip install -e .


Run
---

.. code-block:: text

    $ pboot --app pbootr init-db
    $ pboot --app pbootr run --debug

Open http://127.0.0.1:5000 in a browser.


Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
