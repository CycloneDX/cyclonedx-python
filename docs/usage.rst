Usage
=====

Once installed, you can call the tool's command line interface via the following methods:

.. code-block:: shell

    cyclonedx-py             # call script
    python3 -m cyclonedx_py  # call python module CLI


The full documentation can be issued by running with ``--help``:

.. code-block:: shell-session

    $ cyclonedx-py --help
    usage: cyclonedx-py [-h] [--version] command ...

    Creates CycloneDX Software Bill of Materials (SBOM) from Python projects and environments.

    positional arguments:
      command
        environment   Build an SBOM from Python (virtual) environment
        requirements  Build an SBOM from Pip requirements
        pipenv        Build an SBOM from Pipenv manifest
        poetry        Build an SBOM from Poetry project

    options:
      -h, --help      show this help message and exit
      --version       show program's version number and exit


For Python (virtual) environment
--------------------------------

.. TODO: describe what an environment is...

This will produce the most accurate and complete CycloneDX BOM as it analyses the actually installed packages.
It will include all transitive dependencies required by the packages, as well as their properties.

When using *Environment* as the source, any license information available from the installed packages will also be
included in the generated CycloneDX BOM.

The full documentation can be issued by running with ``--help``:

.. code-block:: shell-session

    $ cyclonedx-py environment --help
    usage: cyclonedx-py environment [-h] [-v]
                                    [--short-PURLs] [--output-reproducible] [--validate | --no-validate]
                                    [-o FILE] [--sv VERSION] [--of FORMAT]
                                    [--pyproject FILE] [--mc-type TYPE]
                                    [python]

    Build an SBOM from Python (virtual) environment

    positional arguments:
      python                Python interpreter

    options:
      -h, --help            show this help message and exit
      --pyproject FILE      Path to the root component's `pyproject.toml` file. This should point to a file compliant with PEP 621 (storing project metadata).
      --mc-type TYPE        Type of the main component {choices: application, firmware, library} (default: ComponentType.APPLICATION)
      --short-PURLs         Omit all qualifiers from PackageURLs. This causes information loss in trade-off shorter PURLs, which might improve ingesting these strings.
      -o FILE, --outfile FILE
                            Output file path for your SBOM (set to "-" to output to STDOUT) (default: -)
      --sv VERSION, --schema-version VERSION
                            The CycloneDX schema version for your SBOM {choices: 1.5, 1.4, 1.3, 1.2, 1.1, 1.0} (default: 1.5)
      --of FORMAT, --output-format FORMAT
                            The output format for your SBOM {choices: JSON, XML} (default: JSON)
      --output-reproducible
                            Whether to go the extra mile and make the output reproducible. This might result in loss of time- and random-based-values.
      --validate, --no-validate
                            Whether validate the result before outputting (default: True)
      -v, --verbose         Increase the verbosity of messages (multiple for more effect) (default: silent)


Examples for macOS/Linux and alike
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell-session
   :caption: Build an SBOM from current python environment

    $ cyclonedx-py environment

.. code-block:: shell-session
   :caption: Build an SBOM from a Python (virtual) environment

   $ cyclonedx-py environment '...some/path/bin/python'
   $ cyclonedx-py environment '.../.venv/'

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


Examples for Windows
~~~~~~~~~~~~~~~~~~~~

.. code-block:: doscon
   :caption: Build an SBOM from current python environment

   > cyclonedx-py

.. code-block:: doscon
   :caption: Build an SBOM from a Python (virtual) environment

   > cyclonedx-py "...some\\path\\bin\\python.exe"
   > cyclonedx-py "...some\\path\\.venv\\"

.. code-block:: doscon
   :caption: Build an SBOM from specific Python environment

   > where.exe python3.9.exe
   > cyclonedx-py "%%path to specific python%%"

.. code-block:: doscon
   :caption: Build an SBOM from conda Python environment

   > conda.exe run where.exe python
   > cyclonedx-py "%%path to conda python%%"

.. code-block:: doscon
   :caption: Build an SBOM from Pipenv environment

   > pipenv.exe --py
   > pipenv.exe --venv
   > cyclonedx-py "%%path to pipenv python%%"

.. code-block:: doscon
   :caption: Build an SBOM from Poetry environment

   > poetry.exe env info  --executable
   > cyclonedx-py "%%path to poetry python%%"



For Pipenv
----------

.. TODO


For Poetry
----------

.. TODO

For Requirements
----------------

.. TODO


For Conda
---------

Conda is a package manager for all kinds on environments.

However, since it might manage a python environment under the hood,
it is possible to utilize the functionality for Python environments as described above.


*****


Programmatic Usage
------------------

This tool utilizes the `CycloneDX Python library`_ to generate the actual data structures, and serialize and validate them.

This tool does **not** expose any additional *public* API or classes - all code is intended to be internal and might change without any notice during version upgrades.

.. _CycloneDX Python library: https://pypi.org/project/cyclonedx-python-lib

However, the CLI is stable - you may call it programmatically like:

.. code-block:: python

   from sys import executable
   from subprocess import run
   run((executable, '-m', 'cyclonedx_py', '--help'))

