# Changelog

<!--next-version-placeholder-->

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
