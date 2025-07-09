Usage
=====

Once installed, you can call the tool's command line interface via the following methods:

.. code-block:: shell

    cyclonedx-py             # call script
    python3 -m cyclonedx_py  # call python module CLI


The full documentation can be issued by running with ``--help``:

.. code-block:: shell-session

    $ cyclonedx-py --help
    usage: cyclonedx-py [-h] [--version] <command> ...

    Creates CycloneDX Software Bill of Materials (SBOM) from Python projects and environments.

    positional arguments:
      <command>
        environment (env, venv)
                            Build an SBOM from Python (virtual) environment
        requirements        Build an SBOM from Pip requirements
        pipenv              Build an SBOM from Pipenv manifest
        poetry              Build an SBOM from Poetry project

    options:
      -h, --help            show this help message and exit
      --version             show program's version number and exit


Example usage: save SBOM in CycloneDX 1.6 XML format, generated from current python environment

.. code-block:: shell

   cyclonedx-py environment --spec-version 1.6 --output-format XML --output-file my-sbom.xml


For Python (virtual) environment
--------------------------------

**subcommand:** ``environment``

**aliases:** ``env``, ``venv``

.. TODO: describe what an environment is...

By analyzing the actually installed packages, this will produce the most accurate and complete CycloneDX BOM.
The generated CycloneDX SBOM will include metadata, licenses, dependency graph, and more.

The full documentation can be issued by running with ``environment --help``:

.. code-block:: shell-session

    $ cyclonedx-py environment --help
    usage: cyclonedx-py environment [-h] [-v]
                                    [--gather-license-texts]
                                    [--short-PURLs] [--output-reproducible]
                                    [--validate | --no-validate]
                                    [-o <file>] [--sv <version>] [--of <format>]
                                    [--pyproject <file>] [--mc-type <type>]
                                    [<python>]

    Build an SBOM from Python (virtual) environment

    positional arguments:
      <python>              Python interpreter

    options:
      -h, --help            show this help message and exit
      --gather-license-texts
                            Enable license text gathering.
      --pyproject <file>    Path to the root component's `pyproject.toml` file.
                            This should point to a file compliant with PEP 621 (Storing project metadata in pyproject.toml). Supports PEP 639 (Improving License Clarity with Better Package Metadata).
      --mc-type <type>      Type of the main component.
                            {choices: application, firmware, library}
                            (default: application)
      --short-PURLs         Omit all qualifiers from PackageURLs.
                            This causes information loss in trade-off shorter PURLs, which might improve ingesting these strings.
      --schema-version <version>
                            DEPRECATED alias for "--spec-version"
      --sv <version>, --spec-version <version>
                            Which version of CycloneDX to use.
                            {choices: 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0}
                            (default: 1.6)
      --output-reproducible
                            Whether to go the extra mile and make the output reproducible.
                            This might result in loss of time- and random-based-values.
      --of <format>, --output-format <format>
                            Which output format to use.
                            {choices: JSON, XML}
                            (default: JSON)
      --outfile <file>      DEPRECATED alias for "--output-file".
      -o <file>, --output-file <file>
                            Path to the output file.
                            (set to "-" to output to STDOUT)
                            (default: -)
      --validate, --no-validate
                            Whether to validate resulting BOM before outputting.
                            (default: True)
      -v, --verbose         Increase the verbosity of messages
                            (multiple for more effect)
                            (default: silent)


Examples for macOS/Linux and alike
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell-session
   :caption: Build an SBOM from python environment

    $ cyclonedx-py environment

.. code-block:: shell-session
   :caption: Build an SBOM from a Python (virtual) environment

   $ cyclonedx-py environment '.../some/path/bin/python'
   $ cyclonedx-py environment '.../some/path/.venv'
   $ cyclonedx-py environment "$VIRTUAL_ENV"

.. code-block:: shell-session
   :caption: Build an SBOM from specific Python environment

   $ cyclonedx-py environment "$(which python3.9)"

.. code-block:: shell-session
   :caption: Build an SBOM from conda Python environment

   $ cyclonedx-py environment "$(conda run which python)"

.. code-block:: shell-session
   :caption: Build an SBOM from Pipenv environment

   $ cyclonedx-py environment "$(pipenv --py)"
   $ cyclonedx-py environment "$(pipenv --venv)"

.. code-block:: shell-session
   :caption: Build an SBOM from Poetry environment

   $ cyclonedx-py environment "$(poetry env info --executable)"

.. code-block:: shell-session
   :caption: Build an SBOM from PDM environment

   $ cyclonedx-py environment "$(pdm info --python)"

.. code-block:: shell-session
   :caption: Build an SBOM from uv environment

   $ cyclonedx-py environment "$(uv python find)"

Examples for Windows
^^^^^^^^^^^^^^^^^^^^

.. code-block:: doscon
   :caption: Build an SBOM from python environment

   > cyclonedx-py environment

.. code-block:: doscon
   :caption: Build an SBOM from a Python (virtual) environment

   > cyclonedx-py environment "...\some\path\bin\python.exe"
   > cyclonedx-py environment "...\some\path\.venv"
   > cyclonedx-py environment "$env:VIRTUAL_ENV"
   > cyclonedx-py environment %VIRTUAL_ENV%

.. code-block:: doscon
   :caption: Build an SBOM from specific Python environment

   > where.exe python3.9.exe
   > cyclonedx-py environment "%path-to-specific-python%"

.. code-block:: doscon
   :caption: Build an SBOM from conda Python environment

   > conda.exe run where.exe python
   > cyclonedx-py environment "%path-to-conda-python%"

.. code-block:: doscon
   :caption: Build an SBOM from Pipenv environment

   > pipenv.exe --py
   > pipenv.exe --venv
   > cyclonedx-py environment "%path-to-pipenv-python%"

.. code-block:: doscon
   :caption: Build an SBOM from Poetry environment

   > poetry.exe env info --executable
   > cyclonedx-py environment "%path-to-poetry-python%"

.. code-block:: doscon
   :caption: Build an SBOM from PDM environment

   > pdm.exe info --python
   > cyclonedx-py environment "%path-to-pdm-python%"

.. code-block:: doscon
   :caption: Build an SBOM from uv environment

   > uv.exe python find
   > cyclonedx-py environment "%path-to-uv-python%"


For Pipenv
----------

**subcommand:** ``pipenv``

Support for `Pipenv`_ dependency management.
This requires parsing your ``Pipfile`` and ``Pipfile.lock`` file which details exact pinned versions of dependencies.

.. _Pipenv: https://pipenv.pypa.io/

The full documentation can be issued by running with ``pipenv --help``:

.. code-block:: shell-session

    $ cyclonedx-py pipenv --help
    usage: cyclonedx-py pipenv [-h] [-v]
                               [--short-PURLs]  [--output-reproducible]
                               [--validate | --no-validate]
                               [-o <file>] [--sv <version>] [--of <format>]
                               [--categories <categories>] [-d]
                               [--pypi-mirror <url>]
                               [--pyproject <file>] [--mc-type <type>]
                               [<project-directory>]

    Build an SBOM from Pipenv manifest.

    The options and switches mimic the respective ones from Pipenv CLI.

    positional arguments:
      <project-directory>   The project directory for Pipenv
                            (default: current working directory)
                            Unlike Pipenv tool, there is no search-up in this very tool. Please
                            provide the actual directory that contains `Pipfile` and `Pipfile.lock` file.

    options:
      -h, --help            show this help message and exit
      --categories <categories>
      -d, --dev             Analyse both develop and default packages
                            [env var: PIPENV_DEV]
      --pypi-mirror <url>   Specify a PyPI mirror
                            [env var: PIPENV_PYPI_MIRROR]
      --pyproject <file>    Path to the root component's `pyproject.toml` file.
                            This should point to a file compliant with PEP 621 (storing project metadata).
      --mc-type <type>      Type of the main component.
                            {choices: application, firmware, library}
                            (default: application)
      --short-PURLs         Omit all qualifiers from PackageURLs.
                            This causes information loss in trade-off shorter PURLs, which might improve ingesting these strings.
      --schema-version <version>
                            DEPRECATED alias for "--spec-version"
      --sv <version>, --spec-version <version>
                            Which version of CycloneDX to use.
                            {choices: 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0}
                            (default: 1.6)
      --output-reproducible
                            Whether to go the extra mile and make the output reproducible.
                            This might result in loss of time- and random-based-values.
      --of <format>, --output-format <format>
                            Which output format to use.
                            {choices: JSON, XML}
                            (default: JSON)
      --outfile <file>      DEPRECATED alias for "--output-file".
      -o <file>, --output-file <file>
                            Path to the output file.
                            (set to "-" to output to STDOUT)
                            (default: -)
      --validate, --no-validate
                            Whether to validate resulting BOM before outputting.
                            (default: True)
      -v, --verbose         Increase the verbosity of messages
                            (multiple for more effect)
                            (default: silent)



For Poetry
----------

**subcommand:** ``poetry``

Support for `Poetry`_ dependency management and package manifest.
This requires parsing your ``pyproject.toml`` and ``poetry.lock`` file which details exact pinned versions of dependencies.

.. _Poetry: https://python-poetry.org/

The full documentation can be issued by running with ``poetry --help``:

.. code-block:: shell-session

    $ cyclonedx-py poetry --help
    usage: cyclonedx-py poetry [-h] [-v]
                               [--short-PURLs] [--output-reproducible]
                               [--validate | --no-validate]
                               [-o <file>] [--sv <version>] [--of <format>]
                               [--without GROUPS] [--with GROUPS] [--only <groups> | --no-dev]
                               [-E EXTRAS | --all-extras]
                               [--mc-type <type>]
                               [<project-directory>]

    Build an SBOM from Poetry project.

    The options and switches mimic the respective ones from Poetry CLI.

    positional arguments:
      <project-directory>   The project directory for Poetry
                            (default: current working directory)

    options:
      -h, --help            show this help message and exit
      --without GROUPS      The dependency groups to ignore
                            (multiple values allowed)
      --with GROUPS         The optional dependency groups to include
                            (multiple values allowed)
      --only GROUPS         The only dependency groups to include
                            (multiple values allowed)
      --no-dev              Alias for: --only main
      -E EXTRAS, --extras EXTRAS
                            Extra sets of dependencies to include
                            (multiple values allowed)
      --all-extras          Include all extra dependencies
                            (default: False)
      --mc-type <type>      Type of the main component.
                            {choices: application, firmware, library}
                            (default: application)
      --short-PURLs         Omit all qualifiers from PackageURLs.
                            This causes information loss in trade-off shorter PURLs, which might improve ingesting these strings.
      --schema-version <version>
                            DEPRECATED alias for "--spec-version"
      --sv <version>, --spec-version <version>
                            Which version of CycloneDX to use.
                            {choices: 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0}
                            (default: 1.6)
      --output-reproducible
                            Whether to go the extra mile and make the output reproducible.
                            This might result in loss of time- and random-based-values.
      --of <format>, --output-format <format>
                            Which output format to use.
                            {choices: JSON, XML}
                            (default: JSON)
      --outfile <file>      DEPRECATED alias for "--output-file".
      -o <file>, --output-file <file>
                            Path to the output file.
                            (set to "-" to output to STDOUT)
                            (default: -)
      --validate, --no-validate
                            Whether to validate resulting BOM before outputting.
                            (default: True)
      -v, --verbose         Increase the verbosity of messages
                            (multiple for more effect)
                            (default: silent)


For Pip requirements
--------------------

**subcommand:** ``requirements``

Support for Pip's `requirements file format`_ dependency lists.

.. _requirements file format: https://pip.pypa.io/en/stable/reference/requirements-file-format/

The full documentation can be issued by running with ``requirements --help``:

.. code-block:: shell-session

    $ cyclonedx-py requirements --help
    usage: cyclonedx-py requirements [-h] [-v]
                                     [--short-PURLs]  [--output-reproducible]
                                     [--validate | --no-validate]
                                     [-o <file>] [--sv <version>] [--of <format>]
                                     [-i <url>] [--extra-index-url <url>]
                                     [--pyproject <file>] [--mc-type <type>]
                                     [<requirements-file>]

    Build an SBOM from Pip requirements.

    The options and switches mimic the respective ones from Pip CLI.

    positional arguments:
      <requirements-file>   Path to requirements file.
                            May be set to "-" to read from <stdin>.
                            (default: 'requirements.txt' in current working directory)

    options:
      -h, --help            show this help message and exit
      -i <url>, --index-url <url>
                            Base URL of the Python Package Index.
                            This should point to a repository compliant with PEP 503 (the simple repository API)
                            or a local directory laid out in the same format.
                            (default: https://pypi.org/simple)
      --extra-index-url <url>
                            Extra URLs of package indexes to use in addition to --index-url.
                            Should follow the same rules as --index-url
      --pyproject <file>    Path to the root component's `pyproject.toml` file.
                            This should point to a file compliant with PEP 621 (storing project metadata).
      --mc-type <type>      Type of the main component.
                            {choices: application, firmware, library}
                            (default: application)
      --short-PURLs         Omit all qualifiers from PackageURLs.
                            This causes information loss in trade-off shorter PURLs, which might improve ingesting these strings.
      --schema-version <version>
                            DEPRECATED alias for "--spec-version"
      --sv <version>, --spec-version <version>
                            Which version of CycloneDX to use.
                            {choices: 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0}
                            (default: 1.6)
      --output-reproducible
                            Whether to go the extra mile and make the output reproducible.
                            This might result in loss of time- and random-based-values.
      --of <format>, --output-format <format>
                            Which output format to use.
                            {choices: JSON, XML}
                            (default: JSON)
      --outfile <file>      DEPRECATED alias for "--output-file".
      -o <file>, --output-file <file>
                            Path to the output file.
                            (set to "-" to output to STDOUT)
                            (default: -)
      --validate, --no-validate
                            Whether to validate resulting BOM before outputting.
                            (default: True)
      -v, --verbose         Increase the verbosity of messages
                            (multiple for more effect)
                            (default: silent)


Example Usage
^^^^^^^^^^^^^

.. code-block:: shell-session
   :caption: Build an SBOM from a requirements file

    $ cyclonedx-py requirements requirements-prod.txt

.. code-block:: shell-session
   :caption: Merge multiple files and build an SBOM from it

    $ cat requirements/*.txt | cyclonedx-py requirements -


.. code-block:: shell-session
   :caption: Build an inventory for all installed packages

    $ python -m pip freeze --all | cyclonedx-py requirements -

.. code-block:: shell-session
   :caption: Build an inventory for all installed packages in a conda environment

    $ conda run python -m pip freeze --all | cyclonedx-py requirements -

.. code-block:: shell-session
   :caption: Build an inventory for installed packages in a Python (virtual) environment

    $ .../.venv/bin/python -m pip freeze --all --local --require-virtualenv | \
      cyclonedx-py requirements -

.. code-block:: shell-session
   :caption: Build an inventory from an unfrozen manifest

    $ python -m pip install -r dependencies.txt && \
      python -m pip freeze | cyclonedx-py requirements -



*****



For PDM
-------

Support for `PDM`_ manifest and lockfile is not explicitly implemented, yet.
See https://github.com/CycloneDX/cyclonedx-python/issues/604

However, since PDM utilizes Python virtual environments under the hood,
it is possible to use the functionality for Python (virtual) environments as described above.

.. _PDM: https://pdm-project.org/



*****



For uv
-------

Support for `uv`_ manifest and lockfile is not explicitly implemented, yet.

However, since uv utilizes Python virtual environments under the hood,
it is possible to use the functionality for Python (virtual) environments as described above.

.. _uv: https://docs.astral.sh/uv/



*****



For Conda
---------

`Conda`_ is a package manager for all kinds on environments.

However, since conda might manage a python environment under the hood,
it is possible to use the functionality for Python (virtual) environments as described above.

.. _Conda: https://conda.io/



*****



Programmatic Usage
------------------

This tool utilizes the `CycloneDX Python library`_ to generate the actual data structures, and serialize and validate them.

This tool does **not** expose any additional *public* API or symbols - all code is intended to be internal and might change without any notice during version upgrades.

.. _CycloneDX Python library: https://pypi.org/project/cyclonedx-python-lib

However, the CLI is stable - you might call it programmatically, like so:

.. keep the following code example in sync with the in-comments example in `__init__.py` and `__main__.py`
.. code-block:: python

   from sys import executable
   from subprocess import run
   run((executable, '-m', 'cyclonedx_py', '--help'))
