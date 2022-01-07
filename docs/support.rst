Support
=======

If you run into issues utilising this library, please raise a `GitHub Issue`_. When raising an issue please include as
much detail as possible including:

* Version ``cyclonedx-bom`` you have installed
* Input(s)
* Expected Output(s)
* Actual Output(s)

Python Version Support
======================

We endeavour to support all functionality for all `current actively supported Python versions`_.
However, some features may not be possible/present in older Python versions due to their lack of support - which are
noted below.

Limitations in Python 3.6.x
---------------------------

* Unit Tests perform schema validation as part of their assertions. The ``jsonschema`` library does not support Python
  3.6 and thus schema validation for JSON tests is skipped when running on Python 3.6.x

.. _GitHub Issue: https://github.com/CycloneDX/cyclonedx-python/issues
.. _current actively supported Python versions: https://www.python.org/downloads/