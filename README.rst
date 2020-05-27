.. image:: https://github.com/CycloneDX/cyclonedx-python/workflows/Python%20CI/badge.svg
   :alt: Build Status
   :target: https://github.com/CycloneDX/cyclonedx-python/actions?workflow=Python+CI

.. image:: https://img.shields.io/badge/docker-image-brightgreen?style=flat&logo=docker
   :alt: Docker Image
   :target: https://hub.docker.com/r/cyclonedx/cyclonedx-python
   
.. image:: https://img.shields.io/badge/license-Apache%202.0-brightgreen
   :alt: License
   :target: https://github.com/CycloneDX/cyclonedx-python/blob/master/LICENSE

.. image:: https://img.shields.io/badge/https://-cyclonedx.org-blue
   :alt: Website
   :target: https://cyclonedx.org/
   
.. image:: https://img.shields.io/badge/Slack-Join-blue?logo=slack&labelColor=393939
   :alt: Slack Invite
   :target: https://cyclonedx.org/slack/invite

.. image:: https://img.shields.io/pypi/v/cyclonedx-bom
   :alt: PyPI
   :target: https://pypi.org/project/cyclonedx-bom/

.. image:: https://img.shields.io/badge/discussion-groups.io-blue
   :alt: Group Discussion
   :target: https://groups.io/g/CycloneDX

.. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow
   :alt: Twitter
   :target: https://twitter.com/CycloneDX_Spec

CycloneDX Python Module
=======================

The CycloneDX module for Python creates a valid CycloneDX bill-of-material document containing an aggregate of all project dependencies. CycloneDX is a lightweight BOM specification that is easily created, human readable, and simple to parse.

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
        -j        - generate JSON instead of XML


License
-------

Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.
