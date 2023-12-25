# Changelog

<!--next-version-placeholder-->

## v3.11.7 (2023-11-03)

### Fix

* Toml-compatible fingers-crossed handling for failed input data decoding ([#613](https://github.com/CycloneDX/cyclonedx-python/issues/613)) ([`fb3d7bf`](https://github.com/CycloneDX/cyclonedx-python/commit/fb3d7bfd1216ad8b5328a1d348fea04fee31d3a4))

## v3.11.6 (2023-11-03)

### Fix

* Added a fingers-crossed handling for failed input data decoding ([#612](https://github.com/CycloneDX/cyclonedx-python/issues/612)) ([`be55902`](https://github.com/CycloneDX/cyclonedx-python/commit/be559020e482795c6603f36e98713c6f7bde1e34))

## v3.11.5 (2023-10-20)

### Fix

* Custom input encoding ([#601](https://github.com/CycloneDX/cyclonedx-python/issues/601)) ([`363934c`](https://github.com/CycloneDX/cyclonedx-python/commit/363934c0bc69ebbb23472f1173bf3c6b1e3c023a))

## v3.11.4 (2023-10-19)

### Fix

* Input file encoding fallback ([`0bc7296`](https://github.com/CycloneDX/cyclonedx-python/commit/0bc72964d0578f713f405bc101742ef096bf8fd7))

## v3.11.3 (2023-10-19)

### Fix

* Input file encoding ([#596](https://github.com/CycloneDX/cyclonedx-python/issues/596)) ([`a9dda4b`](https://github.com/CycloneDX/cyclonedx-python/commit/a9dda4bfd0e68529628eab99b6db00fb5214bfc3))

### Documentation

* Publish coverage ([#600](https://github.com/CycloneDX/cyclonedx-python/issues/600)) ([`bd4f48e`](https://github.com/CycloneDX/cyclonedx-python/commit/bd4f48ef7f3c4c890a138c45dbc87f6ca3e2cf7b))
* Adjust syntax hilight for code blocks ([#592](https://github.com/CycloneDX/cyclonedx-python/issues/592)) ([`ccac31e`](https://github.com/CycloneDX/cyclonedx-python/commit/ccac31eb4d0996236da24ca9efb57af66bd1a020))
* Mark `ShellSession` in README ([`411cf3d`](https://github.com/CycloneDX/cyclonedx-python/commit/411cf3d0a4b5005c1591211ecdc464d4747d69f1))

## v3.11.2 (2023-07-12)

### Fix

* Referenced branch `main`, instead of `master` ([#562](https://github.com/CycloneDX/cyclonedx-python/issues/562)) ([`830d15c`](https://github.com/CycloneDX/cyclonedx-python/commit/830d15c27fadb475fa9a15918b1d5930cd71834d))

## v3.11.1 (2023-07-12)

### Fix

* Fix typo in help page ([#552](https://github.com/CycloneDX/cyclonedx-python/issues/552)) ([`19bf41a`](https://github.com/CycloneDX/cyclonedx-python/commit/19bf41a52a698ee3ddee5fafc5d293ea3d9427be))

## v3.11.0 (2023-02-11)
### Feature
* Deprecated CLI command `cyclonedx-bom` prints deprecation warning on STDERR before execution ([#489](https://github.com/CycloneDX/cyclonedx-python/issues/489)) ([`2009236`](https://github.com/CycloneDX/cyclonedx-python/commit/2009236c537af212aab1d5907e02f2b003f3062c))

### Documentation
* Fix typo in CLI help page ([#490](https://github.com/CycloneDX/cyclonedx-python/issues/490)) ([`a8a8445`](https://github.com/CycloneDX/cyclonedx-python/commit/a8a844504494d10c217ba4739e6ff09b4ca34f67))
* Fix typos ([#482](https://github.com/CycloneDX/cyclonedx-python/issues/482)) ([`edbe3d4`](https://github.com/CycloneDX/cyclonedx-python/commit/edbe3d4e0ee62396ac10b42dd9ee5d6094817675))
* Fix shields ([#473](https://github.com/CycloneDX/cyclonedx-python/issues/473)) ([`e32b288`](https://github.com/CycloneDX/cyclonedx-python/commit/e32b28894a8859925f22a1f45aec8608e7cd8bc3))

## v3.10.1 (2022-12-15)
### Fix
* PURL for PyPI packages from 'conda list' have the correct format now ([#471](https://github.com/CycloneDX/cyclonedx-python/issues/471)) ([`1573064`](https://github.com/CycloneDX/cyclonedx-python/commit/157306483a21583d752714a77ad7d0c7395291e5))

### Documentation
* Improve CONTRIBUTION instructions - sign-off step ([#470](https://github.com/CycloneDX/cyclonedx-python/issues/470)) ([`578c0a8`](https://github.com/CycloneDX/cyclonedx-python/commit/578c0a88e63c804b1462e3d3b617f56b53b6012e))

## v3.10.0 (2022-12-13)
### Feature
* Add support for poetry lock format v2.0 ([#469](https://github.com/CycloneDX/cyclonedx-python/issues/469)) ([`0b1e07f`](https://github.com/CycloneDX/cyclonedx-python/commit/0b1e07f91aada201088605a84ea394182ce0f10e))

## v3.9.0 (2022-12-13)
### Feature
* Parsers can outbut more debug messages ([#466](https://github.com/CycloneDX/cyclonedx-python/issues/466)) ([`9eedb4f`](https://github.com/CycloneDX/cyclonedx-python/commit/9eedb4ff27bb81f4ad323e9fa0f79230b0710032))

## v3.8.0 (2022-12-12)
### Feature
* Error- and debug-output is send to STDERR, instead of STDOUT ([#465](https://github.com/CycloneDX/cyclonedx-python/issues/465)) ([`f543b69`](https://github.com/CycloneDX/cyclonedx-python/commit/f543b69ee4463df3fb4d4b7c86475562f62e4744))

## v3.7.4 (2022-12-12)
### Fix
* Ignore broken licenses in env parser ([#463](https://github.com/CycloneDX/cyclonedx-python/issues/463)) ([`3118acd`](https://github.com/CycloneDX/cyclonedx-python/commit/3118acdf180b6d8d35a637b3e94dc6ec7c5c5b3d))

## v3.7.3 (2022-12-11)
### Fix
* Adjust dependency `pip-requirements-parser` to a working version ([#450](https://github.com/CycloneDX/cyclonedx-python/issues/450)) ([`6101986`](https://github.com/CycloneDX/cyclonedx-python/commit/610198659be408b5ef17d649aa381944d992a7dd))

## v3.7.2 (2022-11-15)
### Fix
* Add a missing space in the help pages `pathto` -> `path to` ([#443](https://github.com/CycloneDX/cyclonedx-python/issues/443)) ([`bc5fe57`](https://github.com/CycloneDX/cyclonedx-python/commit/bc5fe5760565e608387ad7638126869550d65213))

## v3.7.1 (2022-11-10)
### Fix
* **EnvironmentParser:** Reduced crashes if no Classifiers are found ([#441](https://github.com/CycloneDX/cyclonedx-python/issues/441)) ([`67f56e7`](https://github.com/CycloneDX/cyclonedx-python/commit/67f56e7bfa4fb9d50654ebd07ece1ad14377a355))

## v3.7.0 (2022-11-10)
### Feature
* Pass purl-bom-ref to EnvironmentParser ([#432](https://github.com/CycloneDX/cyclonedx-python/issues/432)) ([`7cfefeb`](https://github.com/CycloneDX/cyclonedx-python/commit/7cfefeb389b3c63b69ad93aeca1a709231da2901))

## v3.6.4 (2022-11-10)
### Fix
* **EnvironmentParser:** Remove code break when classifier parsing in py>=3.8 ([#431](https://github.com/CycloneDX/cyclonedx-python/issues/431)) ([`4ab075e`](https://github.com/CycloneDX/cyclonedx-python/commit/4ab075ee814571a8dc8c1e7b962686b232619330))

## v3.6.3 (2022-09-19)
### Fix
* CI release pipeline ([`99ccdc6`](https://github.com/CycloneDX/cyclonedx-python/commit/99ccdc671f5a7a941f31199813bce71405bbfdd8))

## v3.6.2 (2022-09-19)
### Fix
* CI release pipeline ([`6515071`](https://github.com/CycloneDX/cyclonedx-python/commit/6515071fc95d2b460577d0fbceb7d6c34a18c508))

## v3.6.1 (2022-09-19)
### Fix
* Properly declare licenses from environment ([#417](https://github.com/CycloneDX/cyclonedx-python/issues/417)) ([`25f9e29`](https://github.com/CycloneDX/cyclonedx-python/commit/25f9e29a162f20918b6f1bbe887cc7b18c623c16))

## v3.6.0 (2022-09-16)
### Feature
* Enable dependency `cyclonedx-python-lib@^3` ([#418](https://github.com/CycloneDX/cyclonedx-python/issues/418)) ([`05cd51e`](https://github.com/CycloneDX/cyclonedx-python/commit/05cd51e1da261d29fb5c3e1722544a8f00a0cfcd))

### Documentation
* Describe `cyclonedx-py` rather than `cyclonedx-bom` ([`c04196e`](https://github.com/CycloneDX/cyclonedx-python/commit/c04196e4404efc0513676e5baefeaf03e6b3b8e3))
* Minor updates to poetry usage details & contributing.md ([#407](https://github.com/CycloneDX/cyclonedx-python/issues/407)) ([`0abe230`](https://github.com/CycloneDX/cyclonedx-python/commit/0abe23049b5423f55b3e0951a00047f4e3f93056))

## v3.5.0 (2022-06-27)
### Feature
* Optionally force `bom_ref` to be `purl` rather that the default random UUID format - thanks @RodneyRichardson ([`9659d08`](https://github.com/CycloneDX/cyclonedx-python/commit/9659d08f524fd1ea2eb34234f2449105feb93f62))

## v3.4.0 (2022-06-16)
### Feature
* Update purl to match specification when ingesting packages from Conda - thanks to @RodneyRichardson ([`072c8f1`](https://github.com/CycloneDX/cyclonedx-python/commit/072c8f11bdef44abb0c6f7f7e99e2b833ab1c875))

## v3.3.0 (2022-06-16)
### Feature
* Add Conda MD5 hash to Component.hashes, if available - thanks @RodneyRichardson  ([`772c517`](https://github.com/CycloneDX/cyclonedx-python/commit/772c517521da0fd8ddbd1ed8abdf22243f418217))

## v3.2.2 (2022-06-02)
### Fix
* Add actively used (transitive) dependencies ([#363](https://github.com/CycloneDX/cyclonedx-python/issues/363)) ([`1f45ad9`](https://github.com/CycloneDX/cyclonedx-python/commit/1f45ad9162be511f07e9310414793218c554a097))

## v3.2.1 (2022-04-05)
### Fix
* Cli default file for json format ([`8747620`](https://github.com/CycloneDX/cyclonedx-python/commit/8747620dac7ed3eeff69369c05dfb6386a56e549))

## v3.2.0 (2022-04-05)
### Feature
* Make module callable ([`5b3d8d7`](https://github.com/CycloneDX/cyclonedx-python/commit/5b3d8d7641b0f2825e5419b5ad8c8a75bf66403b))

### Documentation
* Describe methods to call the tool ([`2bac83a`](https://github.com/CycloneDX/cyclonedx-python/commit/2bac83a6c6f7354d8b7218c32b4b2e5d96b2fd0c))

## v3.1.1 (2022-03-21)
### Fix
* **conda-parser:** Version recognition for strings ([#332](https://github.com/CycloneDX/cyclonedx-python/issues/332)) ([`65246dd`](https://github.com/CycloneDX/cyclonedx-python/commit/65246ddfa9a55ce53fbf87f33b1f269c519f9b3a))

### Documentation
* Add link to https://cyclonedx.org/ to README ([`fc4b8e4`](https://github.com/CycloneDX/cyclonedx-python/commit/fc4b8e44bec39b175bb8994e0a59bc5076d1b2a6))
* Add hint for RTFD to README ([`cf4f534`](https://github.com/CycloneDX/cyclonedx-python/commit/cf4f534401dc90dbe093ce1a094efb02e5fb7c90))
* Add RTFD shield to README ([`7fef6ee`](https://github.com/CycloneDX/cyclonedx-python/commit/7fef6eec5d553c7687e7b2d2af1ba4e330f16490))
* Fixed link to RTFD ([`3a8669a`](https://github.com/CycloneDX/cyclonedx-python/commit/3a8669ad7ba4230d06d1e0965342a5a836a52d1f))

## v3.1.0 (2022-03-10)
### Feature
* Add pip-requirements-parser and update virtualenv to latest version ([`73b2182`](https://github.com/CycloneDX/cyclonedx-python/commit/73b2182550d9635a0a5ab8e4f2226f37cf6b1b35))

### Fix
* Sort imports ([`fdec44b`](https://github.com/CycloneDX/cyclonedx-python/commit/fdec44bc111d7eb1add080a219dbc77744678f8a))
* Try to fix the temp file issue on Windows machines ([`684d4f0`](https://github.com/CycloneDX/cyclonedx-python/commit/684d4f03ad6f8c0764dfaf8f3a38a09b91b69e5d))

### Documentation
* Update RequirementsFileParser docs to include nested file support ([`9e9021d`](https://github.com/CycloneDX/cyclonedx-python/commit/9e9021decb19d8262e87fe6955577c1bd1309d95))

## v3.0.0 (2022-02-21)
### Feature
* Bump to latest `cyclonedx-python-lib` ([`5902fbf`](https://github.com/CycloneDX/cyclonedx-python/commit/5902fbf9dc5becdf7d92180242488e56b998d9de))
* Added marker and classifiers to denote this as typed ([#313](https://github.com/CycloneDX/cyclonedx-python/issues/313)) ([`f317353`](https://github.com/CycloneDX/cyclonedx-python/commit/f317353bd7a24dbf4fb31642d766d94da609eb42))
* Update to latest RC of `cyclonedx-python-lib` ([`6c8b517`](https://github.com/CycloneDX/cyclonedx-python/commit/6c8b5173f07329b2086312d27af5d111f9b2c7ed))
* Update to latest RC of `cyclonedx-python-lib` ([`bc8ee6b`](https://github.com/CycloneDX/cyclonedx-python/commit/bc8ee6bb115dd5214358430f64bd0581de5cb2e4))

### Breaking
* Default Schema Version has been replaced by notion of LATEST supported Schema Version ([`5902fbf`](https://github.com/CycloneDX/cyclonedx-python/commit/5902fbf9dc5becdf7d92180242488e56b998d9de))

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
