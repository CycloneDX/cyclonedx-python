# CycloneDX Python SBOM Generation Tool

[![shield_pypi-version]][link_pypi]
[![shield_docker-version]][link_docker]
[![shield_rtfd]][link_rtfd]
[![shield_gh-workflow-test]][link_gh-workflow-test]
[![shield_coverage]][link_codacy]
[![shield_license]][license_file]  
[![shield_website]][link_website]
[![shield_slack]][link_slack]
[![shield_groups]][link_discussion]
[![shield_twitter-follow]][link_twitter]

----

This project provides a runnable Python-based application for generating CycloneDX bill-of-material documents from either:

* Your current Python Environment
* Your project's manifest (e.g. `Pipfile.lock`, `poetry.lock` or `requirements.txt`)
* Conda as a Package Manager

The BOM will contain an aggregate of all your current project's dependencies, or those defined by the manifest you supply.

[CycloneDX](https://cyclonedx.org/) is a lightweight BOM specification that is easily created, human-readable, and simple to parse.

Read the full [documentation][link_rtfd] for more details.

## Installation

Install this from [PyPi.org][link_pypi] using your preferred Python package manager.

Example using `pip`:

```shell
pip install cyclonedx-bom
```

Example using `poetry`:

```shell
poetry add cyclonedx-bom
```

## Usage

Call via one of commands:

```shell
cyclonedx-py
python3 -m cyclonedx_py
```

## Basic usage

```shellSession
$ cyclonedx-py --help
usage: cyclonedx-py [-h] (-c | -cj | -e | -p | -pip | -r) [-i FILE_PATH]
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
                        Use with -i to specify absolute path to a `poetry.lock`
                        you wish to use, else we'll look for one in the
                        current working directory.
  -pip, --pip           Build a SBOM based on a PipEnv Pipfile.lock's
                        contents. Use with -i to specify absolute path to a
                        `Pipfile.lock` you wish to use, else we'll look for
                        one in the current working directory.
  -r, --r, --requirements
                        Build a SBOM based on a requirements.txt's contents.
                        Use with -i to specify absolute path to a
                        `requirements.txt` you wish to use, else we'll look
                        for one in the current working directory.
  -X                    Enable debug output

Input Method:
  Flags to determine how this tool obtains its input

  -i FILE_PATH, --in-file FILE_PATH
                        File to read input from. Use "-" to read from STDIN.

SBOM Output Configuration:
  Choose the output format and schema version

  --format {json,xml}   The output format for your SBOM (default: xml)
  --schema-version {1.4,1.3,1.2,1.1,1.0}
                        The CycloneDX schema version for your SBOM (default:
                        1.4)
  -o FILE_PATH, --o FILE_PATH, --output FILE_PATH
                        Output file path for your SBOM (set to '-' to output
                        to STDOUT)
  -F, --force           If outputting to a file and the stated file already
                        exists, it will be overwritten.
  -pb, --purl-bom-ref   Use a component's PURL for the bom-ref value, instead
                        of a random UUID
```

### Advanced usage and details

See the full [documentation][link_rtfd] for advanced usage and details on input formats, switches and options.

## Python Support

We endeavour to support all functionality for all [current actively supported Python versions](https://www.python.org/downloads/).
However, some features may not be possible/present in older Python versions due to their lack of support.

## Contributing

Feel free to open issues, bugreports or pull requests.  
See the [CONTRIBUTING][contributing_file] file for details.

## Copyright & License

CycloneDX BOM is Copyright (c) OWASP Foundation. All Rights Reserved.  
Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.  
See the [LICENSE][license_file] file for the full license.

[license_file]: https://github.com/CycloneDX/cyclonedx-python/blob/main/LICENSE
[contributing_file]: https://github.com/CycloneDX/cyclonedx-python/blob/main/CONTRIBUTING.md
[link_rtfd]: https://cyclonedx-bom-tool.readthedocs.io/

[shield_gh-workflow-test]: https://img.shields.io/github/actions/workflow/status/CycloneDX/cyclonedx-python/python.yml?branch=main&logo=GitHub&logoColor=white "build"
[shield_rtfd]: https://img.shields.io/readthedocs/cyclonedx-bom-tool?logo=readthedocs&logoColor=white
[shield_pypi-version]: https://img.shields.io/pypi/v/cyclonedx-bom?logo=Python&logoColor=white&label=PyPI "PyPI"
[shield_docker-version]: https://img.shields.io/docker/v/cyclonedx/cyclonedx-python?logo=docker&logoColor=white&label=docker "docker"
[shield_license]: https://img.shields.io/github/license/CycloneDX/cyclonedx-python?logo=open%20source%20initiative&logoColor=white "license"
[shield_website]: https://img.shields.io/badge/https://-cyclonedx.org-blue.svg "homepage"
[shield_slack]: https://img.shields.io/badge/slack-join-blue?logo=Slack&logoColor=white "slack join"
[shield_groups]: https://img.shields.io/badge/discussion-groups.io-blue.svg "groups discussion"
[shield_twitter-follow]: https://img.shields.io/badge/Twitter-follow-blue?logo=Twitter&logoColor=white "twitter follow"
[link_gh-workflow-test]: https://github.com/CycloneDX/cyclonedx-python/actions/workflows/python.yml?query=branch%3Amain
[shield_coverage]: https://img.shields.io/codacy/coverage/682ceda9a1044832a087afb95ae280fe?logo=Codacy&logoColor=white "test coverage"
[link_pypi]: https://pypi.org/project/cyclonedx-bom/
[link_docker]: https://hub.docker.com/r/cyclonedx/cyclonedx-python
[link_codacy]: https://app.codacy.com/gh/CycloneDX/cyclonedx-python
[link_website]: https://cyclonedx.org/
[link_slack]: https://cyclonedx.org/slack/invite
[link_discussion]: https://groups.io/g/CycloneDX
[link_twitter]: https://twitter.com/CycloneDX_Spec
