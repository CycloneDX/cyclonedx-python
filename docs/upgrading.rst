Upgrading to v4
===============

Version 4 is not backwards compatible. Nearly all behaviours and integrations changed.
This document covers all breaking changes and should give guidance how to migrate from previous versions.

This document is not a full :doc:`change log <changelog>`, but a migration path.


Python support
--------------

* This tool requires Python 3.9 or later.
  It is tested with CPython, support for PyPy is best effort.


Entry points
------------

* Access via deprecated ``cyclonedx-bom`` was removed. Call ``cyclonedx-py`` instead.
* Access via ``cyclonedx`` stayed untouched.
* Access via ``python -m cyclonedx_py`` stayed untouched.


Changed Command Line Interface (CLI)
------------------------------------

The following describes migration paths only.
For a full list of all features and capabilities, as well as additional examples,
see the :doc:`"usage" documentation</usage>`.

Source: Conda
^^^^^^^^^^^^^

  "Conda provides package, dependency, and environment management for **any** language"

  -- https://docs.conda.io/en/latest/

Conda (lock file) analysis was entirely removed for the fact that conda is not dedicated to Python.
Yes, conda has some capabilities of managing Python packages and environments, but it does so much more.

However, conda's Python environments are fully supported now.
See the :doc:`"usage" documentation</usage>` for examples.

Old: ``cyclonedx-py -c ...`` and ``cyclonedx-py -cj ...``

New: It depends. See the :doc:`"usage" documentation</usage>` for examples.

Source: Environment
^^^^^^^^^^^^^^^^^^^

The functionality was moved to an own subcommand: ``environment``.

Old: ``cyclonedx-py -e``

New: ``cyclonedx-py environment``

Source: Poetry
^^^^^^^^^^^^^^

The functionality was moved to an own subcommand: ``poetry``.
It no longer accepts a lockfile as input, but needs a directory instead.

Old: ``cyclonedx-py -p -i some/path/poetry.lock``

New: ``cyclonedx-py poetry some/path``

Source: Pipenv
^^^^^^^^^^^^^^

The functionality was moved to an own subcommand: ``pipenv``.
It no longer accepts a lockfile as input, but needs a directory instead.

Old: ``cyclonedx-py -pip -i some/path/Pipfile.lock``

New: ``cyclonedx-py pipenv some/path``

Source: Requirements
^^^^^^^^^^^^^^^^^^^^

The functionality was moved to an own subcommand: ``requirements``.

Old: ``cyclonedx-py -r -i some/path/requirements.txt``

New: ``cyclonedx-py requirements some/path/requirements.txt``

Input option
^^^^^^^^^^^^

The CLI option to determine the input parameters were moved to own subcommand arguments.
Therefore all is subcommand-dependant - see the :doc:`"usage" documentation</usage>`.

Output option: Schema version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The CLI option to determine the desired CycloneDX schema version was moved to own subcommand option ``--schema-version``.
Its new default value is ``1.5`` now.

Old: ``cyclonedx-py --schema-version 1.2 ...``

New: Example ``cyclonedx-py environment --schema-version 1.2 ...``

Output option: Format
^^^^^^^^^^^^^^^^^^^^^

The CLI option to determine the desired CycloneDX format was moved to own subcommand option: ``--output-format``.
Its default value is ``JSON`` now.

Old: ``cyclonedx-py --output-format json ...``

New: Example ``cyclonedx-py environment --output-format JSON ...``

Output option: File
^^^^^^^^^^^^^^^^^^^

The CLI option to determine the desired output file/target was moved to own subcommand option: ``--outfile``.
Its default value is ``-`` now, meaning print to ``stdout``.

Old: ``cyclonedx-py --output some/path/my.sbom ...``

New: Example ``cyclonedx-py environment --outfile some/path/my.sbom ...``

Output verbosity
^^^^^^^^^^^^^^^^

The CLI was turned to be as non-verbose as possible, per default. It only outputs the resulting SBOM on ``stdout``.
All other output, like warnings or error messages, is sent to ``stderr``.

Additional output can be enabled with the subcommand option ``-v``.

Example: ``cyclonedx-py environment -v ...``

Enable debug
^^^^^^^^^^^^

* The option ``-X`` was removed. Use subcommand option ``-v`` two times instead, like so: ``-vv``.

Example: ``cyclonedx-py environment -vv ...``

BomRefs based on PURL
^^^^^^^^^^^^^^^^^^^^^

The option ``--purl-bom-ref`` was entirely removed.

Per CycloneDX specifications, ``bom-ref`` values were never intended to shp any meaning, but being linkable.
Therefore, ``bom-ref`` values are arbitrary stings, period.

PURL values
^^^^^^^^^^^

PURL values may be longer now, to shop more meaning. All according to `PackageURL spec`_

.. _PackageURL spec: https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst

It is a known fact, that some SBOM ingesting tools have issues with PURL values being longer than *x* characters.
You may use the CLI option ``--short-PURLs``, which causes information loss in trade-off shorter PURL values.

Removed API
-----------

* All public API was removed.
  You might call the stable CLI instead, like so:

  .. keep the following code example in sync with the in-comments example in `__init__.py` and `__main__.py`
  .. code-block:: python

     from sys import executable
     from subprocess import run
     run((executable, '-m', 'cyclonedx_py', '--help'))
