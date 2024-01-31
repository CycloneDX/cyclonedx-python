Upgrading to v4
===============

Version 4 is not backwards compatible. Nearly all behaviours and integrations changed.
This document covers all breaking changes and should give guidance how to migrate from previous versions.


Python support
--------------

* This tool requires Python 3.8 or later.
  It is tested with CPython, support for PyPy is best effort.


Entry points
------------

* Access via deprecated ``cyclonedx-bom`` was removed. Call ``cyclonedx-py`` instead.
* Access via ``cyclonedx`` stayed untouched.
* Access via ``python -m cyclonedx_py`` stayed untouched.


Changed Command Line Interface (CLI)
------------------------------------

The following describes migration paths only. For all full list of all features
see the :doc:`"usage" documentation</usage>`.

Source: Conda
~~~~~~~~~~~~~

  "Conda provides package, dependency, and environment management for **any** language"

  -- https://docs.conda.io/en/latest/

Conda (lock file) analysis was entirely removed for the fact that conda is not dedicated to Python.
Yes, conda has some capabilities of managing Python packages and environments, but it does so much more.

However, conda's Python environments are fully supported, as well as other means.
See the :doc:`"usage" documentation</usage>` for examples.

Old: ``cyclonedx-py [-c|-cj] ...``

New: It depends. See the :doc:`"usage" documentation</usage>` for examples.

Source: Environment
~~~~~~~~~~~~~~~~~~~

The functionality was moved to an own subcommand: ``environment``.

Old: ``cyclonedx-py -e``

New: ``cyclonedx-py environment``

Source: Poetry
~~~~~~~~~~~~~~

The functionality was moved to an own subcommand: ``poetry``.

Old: ``cyclonedx-py -p -i some/path/poetry.lock``

New: ``cyclonedx-py poetry some/path``

Source: Pipenv
~~~~~~~~~~~~~~

The functionality was moved to an own subcommand: ``pipenv``.

Old: ``cyclonedx-py -pip -i some/path/Pipfile.lock``

New: ``cyclonedx-py pipenv some/path``

Source: Requirements
~~~~~~~~~~~~~~~~~~~~

The functionality was moved to an own subcommand: ``requirements``

Old: ``cyclonedx-py -r -i some/path/requirements.txt``

New: ``cyclonedx-py requirements some/path/requirements.txt``

Output verbosity
~~~~~~~~~~~~~~~~

The CLI was turned to be as non-verbose as possible, per default. It only outputs the resulting SBOM on ``stdout``.
All other output, like warnings or error messages, is sent to ``stderr``.

Additional output can be enabled with the subcommand option ``-v``.

Example: ``cyclonedx-py environment -v``

Enable debug
~~~~~~~~~~~~

* The option ``-X`` was removed. Use subcommand option ``-v`` two times instead, like so: ``-vv``.

Example: ``cyclonedx-py environment -vv``


Removed API
-----------

* All public API was removed.
  You might call the stable CLI instead, like so:

  .. keep the following code example in sync with the in-comments example in `__init__.py` and `__main__.py`
  .. code-block:: python

     from sys import executable
     from subprocess import run
     run((executable, '-m', 'cyclonedx_py', '--help'))
