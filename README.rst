
CycloneDX Python Module
=======================

The CycloneDX module for Python creates a valid CycloneDX bill-of-material document containing an aggregate of all project dependencies. CycloneDX is a lightweight BoM specification that is easily created, human readable, and simple to parse. The resulting bom.xml can be used with tools such as `OWASP Dependency-Track <https://dependencytrack.org/>`_ for the continuous analysis of components.

Usage
-----

**Freezing**

A bill-of-material such as CycloneDX expects exact version numbers. Therefore requirements.txt must be frozen. This can
be accomplished via:

.. code-block:: console

    $ pip freeze > requirements.txt


**Installing**

.. code-block:: console

    $ pip install cyclonedx-bom


**Options**

By default, requirements.txt will be read from the current working directory and the resulting bom.xml will also 
be created in the current working directory. These options can be overwritten as follows:

.. code-block:: console

    $ cyclonedx-py
      Usage:  cyclonedx-py [OPTIONS]
      Options:
        -i <path> - the alternate filename to a frozen requirements.txt
        -o <path> - the bom file to create


License
-------

Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.
