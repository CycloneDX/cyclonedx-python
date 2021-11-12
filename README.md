# CycloneDX Python SBOM Generation Tool

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/CycloneDX/cyclonedx-python/Python%20CI)](https://github.com/CycloneDX/cyclonedx-python/actions/workflows/ci.yml)
[![Docker Image](https://img.shields.io/badge/docker-image-brightgreen?style=flat&logo=docker)](https://hub.docker.com/r/cyclonedx/cyclonedx-python)
[![GitHub license](https://img.shields.io/github/license/CycloneDX/cyclonedx-python)](https://github.com/CycloneDX/cyclonedx-python/blob/main/LICENSE)
[![Python Version Support](https://img.shields.io/badge/https://-cyclonedx.org-blue)](https://cyclonedx.org/)
[![Slack Invite](https://img.shields.io/badge/Slack-Join-blue?logo=slack&labelColor=393939)](https://cyclonedx.org/slack/invite)
![PyPI Version](https://img.shields.io/pypi/v/cyclonedx-bom?label=PyPI&logo=pypi)
![Python Version Support](https://img.shields.io/badge/python-3.6+-blue)
[![Group Discussion](https://img.shields.io/badge/discussion-groups.io-blue)](https://groups.io/g/CycloneDX)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/CycloneDX_Spec)

----

This project provides a runnable Python-based application for generating CycloneDX bill-of-material documents from either:
1. Your current Python Environment
2. Your project's manifest (e.g. `Pipfile.lock`, `poetry.lock` or `requirements.txt`)
3. Conda as a Package Manager

The BOM will contain an aggregate of all your current project's dependencies, or those defined by the manifest you supply.

CycloneDX is a lightweight BOM specification that is easily created, human-readable, and simple to parse.

## Installation

Install this from [PyPi.org](https://pypi.org/project/cyclonedx-bom/) using your preferred Python package manager.

Example using `pip`:
```
pip install cyclonedx-bom
```

Example using `poetry`:
```
poetry add cyclonedx-bom
```

## Usage

Once installed, you can access the full documentation by running `--help`:

```
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
```

### Building CycloneDX for your current Python environment

This will produce the most accurate and complete CycloneDX BOM as it will include all transitive dependencies required
by the packages defined in your project's manifest (think `requriements.txt`).

When using _Environment_ as the source, any license information available from the installed packages will also be 
included in the generated CycloneDX BOM.

Simply run:

```
cyclonedx-bom -e -o -
```

This will generate a CycloneDX including all packages installed in your current Python environment and output to STDOUT
in XML using the latest schema version `1.3` by default.


### Building CycloneDX from your Manifest / Package Manager

_Note: Manifest scanning limits the amount of information available. Each manifest type contains different information
but all are significantly less complete than scanning your actual Python Environment._

#### Conda

We support parsing output from Conda in various formats:
- Explict output (run `conda list --explicit` or `conda list --explicit --md5`)
- JSON output (run `conda list --json`)

As example:
```
conda list --explicit --md5 | cyclonedx-bom -c -o cyclonedx.xml
```

#### Poetry

We support parsing your `poetry.lock` file which should be committed along with your `pyrpoject.toml` and details
exact pinned versions.

You can then run `cyclonedx-bom` as follows:
```
cyclonedx-bom -p -i PATH/TO/poetry.lock -o sbom.xml
```

If your `poetry.lock` is in the current working directory, you can also shorten this to:
```
cyclonedx-bom -p -o sbom.xml
```

#### Pip

We currently support `Pipfile.lock` manifest files.

You can then run `cyclonedx-bom` as follows:
```
cyclonedx-bom -pip -i PATH/TO/Pipfile.lock -o sbom.xml
```

If your `Pipfile.lock` is in the current working directory, you can also shorten this to:
```
cyclonedx-bom -pip -o sbom.xml
```

#### Requirements

We currently support `requirements.txt` manifest files. Note that a BOM such as CycloneDX expects exact version numbers, 
therefore if you wish to generate a BOM from a `requirements.txt`, these must be frozen. This can be accomplished via:

```
pip freeze > requirements.txt
```

You can then run `cyclonedx-bom` as follows:
```
cyclonedx-bom -r -i PATH/TO/requirements.txt -o sbom.xml
```

If your `requirements.txt` is in the current working directory, you can also shorten this to:
```
cyclonedx-bom -r -o sbom.xml
```

This will generate a CycloneDX and output to STDOUT in XML using the latest schema version `1.3` by default.

**Note:** If you failed to freeze your dependencies before passing the `requirements.txt` data to `cyclonedx-bom`, 
you'll be warned about this and the dependencies that do not have pinned versions WILL NOT be included in the resulting 
CycloneDX output.

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! Some of your dependencies do not have pinned version !!
!! numbers in your requirements.txt                     !!
!!                                                      !!
!! -> idna                                              !!
!! -> requests                                          !!
!! -> urllib3                                           !!
!!                                                      !!
!! The above will NOT be included in the generated      !!
!! CycloneDX as version is a mandatory field.           !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

## Python Support

We endeavour to support all functionality for all [current actively supported Python versions](https://www.python.org/downloads/).
However, some features may not be possible/present in older Python versions due to their lack of support.

## Copyright & License

CycloneDX BOM is Copyright (c) OWASP Foundation. All Rights Reserved.

Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.