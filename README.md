[![Build Status](https://travis-ci.org/CycloneDX/cyclonedx-python.svg?branch=master)](https://travis-ci.org/CycloneDX/cyclonedx-python)
[![License](https://img.shields.io/badge/license-Apache%202.0-brightgreen.svg)][License]
[![Website](https://img.shields.io/badge/https://-cyclonedx.org-blue.svg)](https://cyclonedx.org/)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/CycloneDX_Spec)


CycloneDX Python Module
=========

The CycloneDX module for Python creates a valid CycloneDX bill-of-material document containing an aggregate of all project dependencies. CycloneDX is a lightweight BoM specification that is easily created, human readable, and simple to parse. The resulting bom.xml can be used with tools such as [OWASP Dependency-Track](https://dependencytrack.org/) for the continuous analysis of components.

Usage
-------------------

#### Installing

```bash
pip install cyclonedx-bom
```

#### Getting Help
```bash
$ cyclonedx-py -h
Usage:  cyclonedx-py [OPTIONS] [path]
Options:
  -h        - this help
  -i <path> - the alternate filename to a frozen requirements.txt
  -o <path> - write to file instead of stdout

```

#### Example
```bash
cyclonedx-py -o bom.xml
```

License
-------------------

Permission to modify and redistribute is granted under the terms of the Apache 2.0 license. See the [LICENSE] file for the full license.

[License]: https://github.com/CycloneDX/cyclonedx-python/blob/master/LICENSE
