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

    usage: cyclonedx-py [OPTIONS] COMMAND [ARGS]...

    Options:
      -w, --warn-only  Prevents exit with non-zero code when issues have been
                       detected
      -X, --debug      Enable debug output
      --help           Show this message and exit.

    Commands:
      make-bom  Generate a CycloneDX BOM from a Python Environment or...
      version   Show which version of CycloneDX BOM Generator you are running


.. toctree::
   :maxdepth: 1
   :caption: Sub Commands:

   usage-make-bom
   usage-version
