# Changelog

<!--next-version-placeholder-->

## v2.0.3 (2022-02-03)
### Fix
* Docker image releae checkout ref w/o `tags` ([#309](https://github.com/CycloneDX/cyclonedx-python/issues/309)) ([`5d8b1e1`](https://github.com/CycloneDX/cyclonedx-python/commit/5d8b1e159c2ced59e810b9e9564e19a29fe263d0))

## v2.0.2 (2022-02-03)
### Fix
* Properly support reading from stdin ([#307](https://github.com/CycloneDX/cyclonedx-python/issues/307)) ([`23f31a0`](https://github.com/CycloneDX/cyclonedx-python/commit/23f31a03a4fbf888f396b88a9413c054358b2a3a))

## v2.0.1 (2022-01-24)
### Fix
* Bump dependencies to get latest `cyclonedx-python-lib` ([`87c3fe7`](https://github.com/CycloneDX/cyclonedx-python/commit/87c3fe7747cd8abd55ad5699bfc87ad9877c8132))

## v2.0.0 (2022-01-13)
### Feature
* Add support for CycloneDX 1.4 specification ([#294](https://github.com/CycloneDX/cyclonedx-python/issues/294)) ([`7bb6d32`](https://github.com/CycloneDX/cyclonedx-python/commit/7bb6d328adec59cdd4c3ab80eb5f39568ca3bc9c))

### Documentation
* Readme maintenance - shields & links ([#266](https://github.com/CycloneDX/cyclonedx-python/issues/266)) ([`a34046f`](https://github.com/CycloneDX/cyclonedx-python/commit/a34046f9b4c96d013fdf2dbdac5e930aa9204e15))

## v1.5.3 (2021-11-23)
### Fix
* Revert to previous process for building Docker image as PyPi index update is too slow to pull straight away after publish ([`67bb738`](https://github.com/CycloneDX/cyclonedx-python/commit/67bb738246bfe0ca3acd409d8c5a27fd7a305347))

## v1.5.2 (2021-11-23)
### Fix
* Corrected docker image build process to not rely on `dist` folder which is cleaned up by python-semantic-release ([`6c65c11`](https://github.com/CycloneDX/cyclonedx-python/commit/6c65c11d439169417e2ef7e94cacb1ec216eb11c))

## v1.5.1 (2021-11-23)
### Fix
* Re-enable build and publish of Docker Image ([#263](https://github.com/CycloneDX/cyclonedx-python/issues/263)) ([`478360d`](https://github.com/CycloneDX/cyclonedx-python/commit/478360db0de269159ab6e3777cd291b87e2e1174))

## v1.5.0 (2021-11-17)
### Feature
* Support for Python 3.10 ([#261](https://github.com/CycloneDX/cyclonedx-python/issues/261)) ([`f4f9ffe`](https://github.com/CycloneDX/cyclonedx-python/commit/f4f9ffe4b1e2d4fffe4ad0b274a067a20c9c372f))

## v1.4.3 (2021-11-16)
### Fix
* Add static code analysis, better typing and bump cyclonedx-python-lib to 0.11 ([`d5d9f56`](https://github.com/CycloneDX/cyclonedx-python/commit/d5d9f563f2ceb1bdfb2f9cb39ff07af9f0deca26))

## v1.4.2 (2021-11-12)
### Fix
* If no input file is supplied and no input is provided on STDIN, we will now try to automatically locate (in the current working directory) a manifest with default name for the input type specified. This works for PIP (Pipfile.lock), Poetry (poetry.lock) and Requirements (requirements.txt) ([`93f9e59`](https://github.com/CycloneDX/cyclonedx-python/commit/93f9e5985f0d0cecd865b66119276d33b2175fe9))

## v1.4.1 (2021-10-26)
### Fix
* Corrected documentation after deprecation of `-rf`, `-pf`, `--poetry-file`, `--requirements-file` and `--pip-file` ([`4c4c8d8`](https://github.com/CycloneDX/cyclonedx-python/commit/4c4c8d8d4756ebc953c26504052d5469f3c47cfa))

## v1.4.0 (2021-10-21)
### Breaking Changes
* The following parameter flags have all been removed in favour of a single common parameter flag `-i`:
  * For Poetry: `-pf`, `--poetry-file`
  * For Requirements: `-rf`, `--requirements-file`

### Feature
* Add conda support (bump cyclonedx-python-lib to ^0.10.0) ([`cb24275`](https://github.com/CycloneDX/cyclonedx-python/commit/cb24275f3e8716244de2b4ef0a046b879fa88ba5))

### Fix
* Encoding issues on Windows (bump cyclonedx-python-lib to ^0.10.2) ([`da6772b`](https://github.com/CycloneDX/cyclonedx-python/commit/da6772be89ad923b1d8df6dd3b2a89c6e5805571))
* Encoding issues on Windows (bump cyclonedx-python-lib to ^0.10.1) ([`fe5df36`](https://github.com/CycloneDX/cyclonedx-python/commit/fe5df3607157b2f24854ef1f69457f163d79a093))

## v1.3.1 (2021-10-19)
### Fix
* Bump to cyclonedx-python-lib to resolve issue #244 ([`ebea3ef`](https://github.com/CycloneDX/cyclonedx-python/commit/ebea3ef47e917479a7474489bb274b5fa9704375))

## v1.3.0 (2021-10-19)
### Feature
* Add license information in CycloneDX BOM when using Environment as the source ([`5d1f9a7`](https://github.com/CycloneDX/cyclonedx-python/commit/5d1f9a76cfa2bc1461a3dcf4c140d81876a37c40))

## v1.2.0 (2021-10-12)
### Feature
* Update to latest stable cyclonedx-python-lib ([`6145bd5`](https://github.com/CycloneDX/cyclonedx-python/commit/6145bd52c450e66f42367e61e086d2a9d9818b47))

## v1.1.0 (2021-10-04)
### Feature
* Add support for generating SBOM from poetry.lock files ([`bb4ac0f`](https://github.com/CycloneDX/cyclonedx-python/commit/bb4ac0f29b46db59b192191f65dfa40757268188))

## v1.0.5 (2021-09-27)
### Fix
* Handle `requirements.txt` which contain dependencies without a version statement and warn that they cannot be included in the resulting CycloneDX BOM ([`e637e56`](https://github.com/CycloneDX/cyclonedx-python/commit/e637e56cada6d841dae193c106647b0b03a4e776))

## v1.0.4 (2021-09-27)
### Fix
* Error message when `requirements.txt` file is non-existent updated ([`3bbc071`](https://github.com/CycloneDX/cyclonedx-python/commit/3bbc071a1ff26599bd9eb3220de38bd9c58fa294))

## v1.0.3 (2021-09-27)
### Fix
* Default to "requirements.txt" in current directory when "-r" flag is supplied but not "-rf" flag is supplied ([`bb7e30a`](https://github.com/CycloneDX/cyclonedx-python/commit/bb7e30a869300b1e63a00d7db4bcc7f35d68552d))

## v1.0.2 (2021-09-13)
### Fix
* Release GH action ([`148421b`](https://github.com/CycloneDX/cyclonedx-python/commit/148421bcd8cea2b5f8f3bd5958f6f7171afe859e))

## v1.0.1 (2021-09-13)
### Fix
* **ci:** Corrected main to master branch. ([`7162cd9`](https://github.com/CycloneDX/cyclonedx-python/commit/7162cd9385729dafbdc15dbb55e9ac5adf3906cf))
