Usage
=======

Command Line Usage
------------------

Once installed, you can call the tool via the following methods:

.. code-block:: bash

    $ python3 -m cyclonedx_py
    $ cyclonedx-py

The full documentation can be issued by running with ``--help``:

.. code-block:: bash

    usage: cyclonedx-py [-h] [-v] [-w] [-X]  ...

    CycloneDX BOM Generator

    options:
      -h, --help       show this help message and exit
      -v, --version    show which version of CycloneDX BOM Generator you are running
      -w, --warn-only  prevents exit with non-zero code when issues have been detected
      -X               enable debug output

    CycloneDX BOM Generator sub-commands:

        make-bom       Make a BOM from your environment as specified


.. toctree::
   :maxdepth: 1
   :caption: Sub Commands:

   usage-make-bom
