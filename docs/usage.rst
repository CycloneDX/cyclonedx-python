Usage
=======

Command Line Usage
------------------

Once installed, you can call the tool via the following methods:

.. code-block:: bash

    $ python3 -m cyclonedx_py
    $ cyclonedx-py
    $ cyclonedx-bom

The full documentation can be issued by running with ``--help``:

.. code-block:: bash

    $ cyclonedx-bom --help
    usage: cyclonedx-bom [-h] (-c | -cj | -e | -p | -pip | -r) [-i FILE_PATH]
                     [--format {json,xml}] [--schema-version {1.4,1.3,1.2,1.1,1.0}]
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
      --schema-version {1.4,1.3,1.2,1.1,1.0}
                            The CycloneDX schema version for your SBOM (default:
                            1.3)
      -o FILE_PATH, --o FILE_PATH, --output FILE_PATH
                            Output file path for your SBOM (set to '-' to output
                            to STDOUT)
      -F, --force           If outputting to a file and the stated file already
                            exists, it will be overwritten.

From your current Python Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This will produce the most accurate and complete CycloneDX BOM as it will include all transitive dependencies required
by the packages defined in your project's manifest (think ``requirements.txt``).

When using *Environment* as the source, any license information available from the installed packages will also be
included in the generated CycloneDX BOM.

Simply run:

.. code-block:: bash

    cyclonedx-bom -e -o -


This will generate a CycloneDX including all packages installed in your current Python environment and output to STDOUT
in XML using the default schema version ``1.3`` by default.

From your Python application manifest

.. note::

    Manifest scanning limits the amount of information available. Each manifest type contains different information
    but all are significantly less complete than scanning your actual Python Environment.


**Conda**

We support parsing output from Conda in various formats:

* Explict output (run ``conda list --explicit`` or ``conda list --explicit --md5``)
* JSON output (run ``conda list --json``)

As example:

.. code-block:: bash

    conda list --explicit --md5 | cyclonedx-bom -c -o cyclonedx.xml

**Poetry**

We support parsing your ``poetry.lock`` file which should be committed along with your ``pyrpoject.toml`` and details
exact pinned versions.

You can then run ``cyclonedx-bom`` as follows:

.. code-block:: bash

    cyclonedx-bom -p -i PATH/TO/poetry.lock -o sbom.xml


If your ``poetry.lock`` is in the current working directory, you can also shorten this to:

.. code-block:: bash

    cyclonedx-bom -p -o sbom.xml

**Pip**

We currently support ``Pipfile.lock`` manifest files.

You can then run ``cyclonedx-bom`` as follows:

.. code-block:: bash

    cyclonedx-bom -pip -i PATH/TO/Pipfile.lock -o sbom.xml


If your ``Pipfile.lock`` is in the current working directory, you can also shorten this to:

.. code-block:: bash

    cyclonedx-bom -pip -o sbom.xml


**Requirements**

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


Programmatic Usage
------------------

This library provides a number of concrete implementations of :py:mod:`cyclondex.parser.BaserParser`.
Parsers are provided as a quick way to generate a BOM for Python applications or from Python environments.

    **WARNING**: Limited information will be available when generating a BOM using some Parsers due to limited
    information kept/supplied by those package managers. See below for details of what fields can be completed by
    different Parsers.

Easily create your parser instance as follows:

.. code-block:: python

   from cyclonedx_py.parser.environment import EnvironmentParser

   parser = EnvironmentParser()

Conda
~~~~~

* :py:mod:`cyclonedx_py.parser.conda.CondaListJsonParser`: Parses input provided as a ``str`` that is output from
  ``conda list --json``
* :py:mod:`cyclonedx_py.parser.conda.CondaListExplicitParser`: Parses input provided as a ``str`` that is output from:
  ``conda list --explicit`` or ``conda list --explicit --md5``

Environment
~~~~~~~~~~~

* :py:mod:`cyclonedx_py.parser.environment.EnvironmentParser`: Looks at the packages installed in your current Python
  environment

Pip
~~~~~~~

* :py:mod:`cyclonedx_py.parser.pipenv.PipEnvParser`: Parses ``Pipfile.lock`` content passed in as a string
* :py:mod:`cyclonedx_py.parser.pipenv.PipEnvFileParser`: Parses the ``Pipfile.lock`` file at the supplied path

Poetry
~~~~~~

* :py:mod:`cyclonedx.parser.poetry.PoetryParser`: Parses ``poetry.lock`` content passed in as a string
* :py:mod:`cyclonedx.parser.poetry.PoetryFileParser`: Parses the ``poetry.lock`` file at the supplied path

Requirements
~~~~~~~~~~~~

* :py:mod:`cyclonedx_py.parser.requirements.RequirementsParser`: Parses a multiline string that you provide that conforms
  to the ``requirements.txt`` :pep:`508` standard.
* :py:mod:`cyclonedx_py.parser.requirements.RequirementsFileParser`: Parses a file that you provide the path to that conforms to the ``requirements.txt`` :pep:`508` standard.
  It supports nested files, so if there is a line in your ``requirements.txt`` file with the ``-r requirements-nested.txt`` syntax, it'll parse the nested file as part of the same file.

CycloneDX software bill-of-materials require pinned versions of requirements. If your `requirements.txt` does not have
pinned versions, warnings will be recorded and the dependencies without pinned versions will be excluded from the
generated CycloneDX. CycloneDX schemas (from version 1.0+) require a component to have a version when included in a
CycloneDX bill of materials (according to schema).

If you need to use a ``requirements.txt`` in your project that does not have pinned versions an acceptable workaround
might be to:

.. code-block:: bash

   pip install -r requirements.txt
   pip freeze > requirements-frozen.txt

You can then feed in the frozen requirements from ``requirements-frozen.txt`` `or` use the ``Environment`` parser once
you have installed your dependencies.

Parser Schema Support
---------------------

Different parsers support population of different information about your dependencies due to how information is
obtained and limitations of what information is available to each Parser. The sections below explain coverage as to what
information is obtained by each set of Parsers. It does NOT guarantee the information is output in the resulting
CycloneDX BOM document.

The below tables do not state whether specific schema versions support the attributes/items, just whether this library
does.

xPath is used to refer to data attributes according to the `Cyclone DX Specification`_.

``bom.components.component``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-------------------------+-------------------------------------------------------------------+
|                         | Parser Support                                                    |
| Data Path               +------------+-------------+------------+------------+--------------+
|                         | Conda      | Environment | Pip        | Poetry     | Requirements |
+=========================+============+=============+============+============+==============+
| ``.supplier``           | N          | N - Note 1  | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.author``             | N          | Y - Note 1  | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.publisher``          | N          | N - Note 1  | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.group``              | N          | N           | N          | N          | N            |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.name``               | Y          | Y           | Y          | Y          | Y            |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.version``            | Y          | Y           | Y          | Y          | Y            |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.description``        | N          | N           | N/A        | N          | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.scope``              | N          | N           | N/A        | N          | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.hashes``             | Y - Note 2 | N/A         | Y - Note 3 | Y - Note 3 | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.licenses``           | N          | Y - Note 1  | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.copyright``          | N          | N - Note 1  | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.cpe``                | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.purl``               | Y          | Y           | Y          | Y          | Y            |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.swid``               | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.modified``           | *Deprecated - not used*                                           |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.pedigree``           | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.externalReferences`` | Y - Note 3 | N/A         | Y - Note 1 | Y - Note 1 | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.properties``         | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.components``         | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.evidence``           | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+
| ``.releaseNotes``       | N/A        | N/A         | N/A        | N/A        | N/A          |
+-------------------------+------------+-------------+------------+------------+--------------+

    **Legend:**

    * **Y**: YES with any caveat states.
    * **N**: Not currently supported, but support believed to be possible.
    * **N/A**: Not supported and not deemed possible (i.e. the Parser would never be able to reliably determine this
      info).

**Notes**

1. If contained in the packaages ``METADATA``
2. MD5 hashses are available when using the ``CondaListExplicitParser`` with output from the
   conda command ``conda list --explicit --md5`` only
3. Python packages are regularly available as both ``.whl`` and ``.tar.gz`` packages. This means for that for a given
   package and version multiple artefacts are possible - which would mean multiple hashes are possible. CycloneDX
   supports only a single set of hashes identifying a single artefact at ``component.hashes``. To cater for this
   situation in Python, we add the hashes to `component.externalReferences`, as we cannot determine which package was
   actually obtained and installed to meet a given dependency.

.. _Cyclone DX Specification: https://cyclonedx.org/docs/latest
