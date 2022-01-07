Usage
=======

Once installed, you can access the full documentation by running ``--help``:

.. code-block:: bash

    $ cyclonedx-bom --help
    usage: cyclonedx-bom [-h] (-c | -cj | -e | -p | -pip | -r) [-i FILE_PATH]
                     [--format {json,xml}] [--schema-version {1.3,1.2,1.1,1.0}]
                     [-o FILE_PATH] [-F] [-X]

    CycloneDX SBOM Generator

    optional arguments:
      -h, --help            show this help message and exit
      -c, --conda           Build a SBOM based on the output from `conda list
                            --explicit` or `conda list --explicit --md5`
      -cj, --conda-json     Build a SBOM based on the output from `conda list
                            --json`
      -e, --e, --environment
                            Build a SBOM based on the packages installed in your
                            current Python environment (default)
      -p, --p, --poetry     Build a SBOM based on a Poetry poetry.lock's contents.
                            Use with -i to specify absolute pathto a `poetry.lock`
                            you wish to use, else we'll look for one in the
                            current working directory.
      -pip, --pip           Build a SBOM based on a PipEnv Pipfile.lock's
                            contents. Use with -i to specify absolute pathto a
                            `Pipefile.lock` you wish to use, else we'll look for
                            one in the current working directory.
      -r, --r, --requirements
                            Build a SBOM based on a requirements.txt's contents.
                            Use with -i to specify absolute pathto a
                            `requirements.txt` you wish to use, else we'll look
                            for one in the current working directory.
      -X                    Enable debug output

    Input Method:
      Flags to determine how `cyclonedx-bom` obtains it's input

      -i FILE_PATH, --in-file FILE_PATH
                            File to read input from, or STDIN if not specified

    SBOM Output Configuration:
      Choose the output format and schema version

      --format {json,xml}   The output format for your SBOM (default: xml)
      --schema-version {1.3,1.2,1.1,1.0}
                            The CycloneDX schema version for your SBOM (default:
                            1.3)
      -o FILE_PATH, --o FILE_PATH, --output FILE_PATH
                            Output file path for your SBOM (set to '-' to output
                            to STDOUT)
      -F, --force           If outputting to a file and the stated file already
                            exists, it will be overwritten.

SBOM for your current Python Environment
----------------------------------------

This will produce the most accurate and complete CycloneDX BOM as it will include all transitive dependencies required
by the packages defined in your project's manifest (think ``requirements.txt``).

When using *Environment* as the source, any license information available from the installed packages will also be
included in the generated CycloneDX BOM.

Simply run:

.. code-block:: bash

    cyclonedx-bom -e -o -


This will generate a CycloneDX including all packages installed in your current Python environment and output to STDOUT
in XML using the default schema version ``1.3`` by default.

SBOM from your Python application manifest
------------------------------------------

.. note::

    Manifest scanning limits the amount of information available. Each manifest type contains different information
    but all are significantly less complete than scanning your actual Python Environment.

Conda
~~~~~

We support parsing output from Conda in various formats:

* Explict output (run ``conda list --explicit`` or ``conda list --explicit --md5``)
* JSON output (run ``conda list --json``)

As example:

.. code-block:: bash

    conda list --explicit --md5 | cyclonedx-bom -c -o cyclonedx.xml

Poetry
~~~~~~

We support parsing your ``poetry.lock`` file which should be committed along with your ``pyrpoject.toml`` and details
exact pinned versions.

You can then run ``cyclonedx-bom`` as follows:

.. code-block:: bash

    cyclonedx-bom -p -i PATH/TO/poetry.lock -o sbom.xml


If your ``poetry.lock`` is in the current working directory, you can also shorten this to:

.. code-block:: bash

    cyclonedx-bom -p -o sbom.xml


Pip
~~~

We currently support ``Pipfile.lock`` manifest files.

You can then run ``cyclonedx-bom`` as follows:

.. code-block:: bash

    cyclonedx-bom -pip -i PATH/TO/Pipfile.lock -o sbom.xml


If your ``Pipfile.lock`` is in the current working directory, you can also shorten this to:

.. code-block:: bash

    cyclonedx-bom -pip -o sbom.xml


Requirements
~~~~~~~~~~~~

We support ``requirements.txt`` manifest files. Note that a SBOM such as CycloneDX expects exact version numbers,
therefore if you wish to generate a BOM from a ``requirements.txt``, these must be frozen. This can be accomplished via:

.. code-block:: bash

    pip freeze > requirements.txt


You can then run ``cyclonedx-bom`` as follows:

.. code-block:: bash

    cyclonedx-bom -r -i PATH/TO/requirements.txt -o sbom.xml

If your ``requirements.txt`` is in the current working directory, you can also shorten this to:

.. code-block:: bash

    cyclonedx-bom -r -o sbom.xml


This will generate a CycloneDX and output to STDOUT in XML using the default schema version `1.3`.

.. note::

    If you failed to freeze your dependencies before passing the ``requirements.txt`` data to ``cyclonedx-bom``,
    you'll be warned about this and the dependencies that do not have pinned versions WILL NOT be included in the
    resulting CycloneDX output.
