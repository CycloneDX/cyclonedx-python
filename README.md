# CycloneDX Python SBOM Generation Tool

[![shield_pypi-version]][link_pypi]
[![shield_docker-version]][link_docker]
[![shield_rtfd]][link_rtfd]
[![shield_gh-workflow-test]][link_gh-workflow-test]
[![shield_coverage]][link_codacy]
[![shield_ossf-best-practices]][link_ossf-best-practices]
[![shield_license]][license_file]  
[![shield_website]][link_website]
[![shield_slack]][link_slack]
[![shield_groups]][link_discussion]
[![shield_twitter-follow]][link_twitter]

----

This tool generates Software Bill of material (SBOM) documents in OWASP [CycloneDX](https://cyclonedx.org/) format.  
Supported data sources are:

* Python (virtual) environment
* `Poetry` manifest and lockfile
* `Pipenv` manifest and lockfile
* Pip's `requirements.txt` format
* `PDM` manifest and lockfile are not explicitly supported.  
  However, PDM's Python virtual environments are fully supported. See the docs for an example.
* `Conda` as a package manager is no longer supported since version 4.  
  However, conda's Python environments are fully supported via the methods listed above. See the docs for an example.

Based on [OWASP Software Component Verification Standard for Software Bill of Materials](https://scvs.owasp.org/scvs/v2-software-bill-of-materials/)'
criteria, this tool is capable of producing SBOM documents almost passing Level-2 (only signing needs to be done externally).

The resulting SBOM documents follow [official specifications and standards](https://github.com/CycloneDX/specification),
and might have properties following 
[`cdx:python` Namespace Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/python.md),
[`cdx:pipenv` Namespace Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/pipenv.md),
[`cdx:poetry` Namespace Taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/poetry.md)
.

Read the full [documentation][link_rtfd] for more details.

## Requirements

* Python `>=3.8,<4`

However, there are older versions of this tool available, which
support Python `>=2.7`.

## Installation

Install this from [Python Package Index (PyPI)][link_pypi] using your preferred Python package manager.

install via one of commands:

```shell
python -m pip install cyclonedx-bom   # install via pip
pipx install cyclonedx-bom            # install via pipx
poetry add cyclonedx-bom              # install via poetry
# ... you get the hang
```

## Usage

Call via one of commands:

```shell
cyclonedx-py             # call script
python3 -m cyclonedx_py  # call python module CLI
```

### Basic usage

```shellSession
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
```

### Advanced usage and details

See the full [documentation][link_rtfd] for advanced usage and details on input formats, switches and options.

## Python Support

We endeavour to support all functionality for all [current actively supported Python versions](https://www.python.org/downloads/).
However, some features may not be possible/present in older Python versions due to their lack of support.
However, there are older versions of this tool, that support `python>=2.7`.

## Internals

This tool utilizes the [CycloneDX Python library][cyclonedx-library] to generate the actual data structures, and serialize and validate them.  

This tool does **not** expose any additional _public_ API or symbols - all code is intended to be internal and might change without any notice during version upgrades.
However, the CLI is stable - you might call it programmatically. See the documentation for an example.

## Contributing

Feel free to open issues, bugreports or pull requests.  
See the [CONTRIBUTING][contributing_file] file for details, and how to run/setup locally.

## Copyright & License

CycloneDX BOM is Copyright (c) OWASP Foundation. All Rights Reserved.  
Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.  
See the [LICENSE][license_file] file for the full license.

[license_file]: https://github.com/CycloneDX/cyclonedx-python/blob/main/LICENSE
[contributing_file]: https://github.com/CycloneDX/cyclonedx-python/blob/main/CONTRIBUTING.md
[link_rtfd]: https://cyclonedx-bom-tool.readthedocs.io/

[cyclonedx-library]: https://pypi.org/project/cyclonedx-python-lib

[shield_gh-workflow-test]: https://img.shields.io/github/actions/workflow/status/CycloneDX/cyclonedx-python/python.yml?branch=main&logo=GitHub&logoColor=white "build"
[shield_rtfd]: https://img.shields.io/readthedocs/cyclonedx-bom-tool?logo=readthedocs&logoColor=white "Read the Docs"
[shield_pypi-version]: https://img.shields.io/pypi/v/cyclonedx-bom?logo=Python&logoColor=white&label=PyPI "PyPI"
[shield_docker-version]: https://img.shields.io/docker/v/cyclonedx/cyclonedx-python?logo=docker&logoColor=white&label=docker "docker"
[shield_license]: https://img.shields.io/github/license/CycloneDX/cyclonedx-python?logo=open%20source%20initiative&logoColor=white "license"
[shield_website]: https://img.shields.io/badge/https://-cyclonedx.org-blue.svg "homepage"
[shield_slack]: https://img.shields.io/badge/slack-join-blue?logo=Slack&logoColor=white "slack join"
[shield_groups]: https://img.shields.io/badge/discussion-groups.io-blue.svg "groups discussion"
[shield_twitter-follow]: https://img.shields.io/badge/Twitter-follow-blue?logo=Twitter&logoColor=white "twitter follow"
[shield_coverage]: https://img.shields.io/codacy/coverage/682ceda9a1044832a087afb95ae280fe?logo=Codacy&logoColor=white "test coverage"
[shield_ossf-best-practices]: https://img.shields.io/cii/percentage/7957?label=OpenSSF%20best%20practices "OpenSSF best practices"

[link_gh-workflow-test]: https://github.com/CycloneDX/cyclonedx-python/actions/workflows/python.yml?query=branch%3Amain
[link_pypi]: https://pypi.org/project/cyclonedx-bom/
[link_docker]: https://hub.docker.com/r/cyclonedx/cyclonedx-python
[link_codacy]: https://app.codacy.com/gh/CycloneDX/cyclonedx-python
[link_ossf-best-practices]: https://www.bestpractices.dev/projects/7957
[link_website]: https://cyclonedx.org/
[link_slack]: https://cyclonedx.org/slack/invite
[link_discussion]: https://groups.io/g/CycloneDX
[link_twitter]: https://twitter.com/CycloneDX_Spec
