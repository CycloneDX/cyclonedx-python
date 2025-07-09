# CHANGELOG

<!-- version list -->

## v7.0.1-alpha.2 (2025-07-09)


## v6.1.3 (2025-07-08)

### Bug Fixes

- License file detection according to PEP621
  ([#929](https://github.com/CycloneDX/cyclonedx-python/pull/929),
  [`28dcbf7`](https://github.com/CycloneDX/cyclonedx-python/commit/28dcbf7949b8f0cfa51f217c6e3939ce9d9926c2))


## v6.1.2 (2025-06-26)

### Bug Fixes

- Make pep621 license detections type-aware
  ([#920](https://github.com/CycloneDX/cyclonedx-python/pull/920),
  [`0c9aeac`](https://github.com/CycloneDX/cyclonedx-python/commit/0c9aeaca0d5dce56fe50df77f2d9384194f8276f))

### Documentation

- Formatting and reorder of code style instructions.
  ([`15ac2cd`](https://github.com/CycloneDX/cyclonedx-python/commit/15ac2cd7b9d3e76163d894cb064a6bc401b46f80))

- License file `*.rst` are NOT type `text` - they are binary
  ([#911](https://github.com/CycloneDX/cyclonedx-python/pull/911),
  [`168f81d`](https://github.com/CycloneDX/cyclonedx-python/commit/168f81d2c951e4fd7c3ceefe3586cc7d70fbb76a))


## v6.1.1 (2025-05-12)

### Bug Fixes

- Maintenance
  ([`e3c168b`](https://github.com/CycloneDX/cyclonedx-python/commit/e3c168b34fd33c38dd23847d2d065b7216c6c256))


## v6.1.0 (2025-05-12)

### Documentation

- Fix default value for `--spec-version `
  ([`2f2982b`](https://github.com/CycloneDX/cyclonedx-python/commit/2f2982b35c5d4a520b75fe51b85796b8163335e0))

### Features

- Rootless docker container ([#893](https://github.com/CycloneDX/cyclonedx-python/pull/893),
  [`a0cd44b`](https://github.com/CycloneDX/cyclonedx-python/commit/a0cd44ba2e9c49f621e10b70f5efde306c9906ac))


## v6.0.0 (2025-04-24)

### Features

- Add mimetype detection for rich text format (rtf)
  ([#886](https://github.com/CycloneDX/cyclonedx-python/pull/886),
  [`9861a46`](https://github.com/CycloneDX/cyclonedx-python/commit/9861a46fb9a12f8b857fa31d393e1eb6656af141))

- Drop support for python <3.9 ([#883](https://github.com/CycloneDX/cyclonedx-python/pull/883),
  [`9a5e6d8`](https://github.com/CycloneDX/cyclonedx-python/commit/9a5e6d8a985262ffa5cf97da5e687470887f4e35))

- Spec-version defaults to CycloneDX 1.6
  ([#885](https://github.com/CycloneDX/cyclonedx-python/pull/885),
  [`880dd79`](https://github.com/CycloneDX/cyclonedx-python/commit/880dd79c4ca6737c08c35288d14323c0db71b166))


## v5.5.0 (2025-04-23)

### Features

- Support runtime-dependency `packaging ^25`
  ([#882](https://github.com/CycloneDX/cyclonedx-python/pull/882),
  [`4fa5a35`](https://github.com/CycloneDX/cyclonedx-python/commit/4fa5a35ad8419f352c2436f86efd070b8729c5af))


## v5.4.0 (2025-04-23)

### Documentation

- Install instructions for `uv`
  ([`07d9bcc`](https://github.com/CycloneDX/cyclonedx-python/commit/07d9bccea8bd5cefa34dec0cb930da719a7dac97))

- Reword common CLI switches ([#877](https://github.com/CycloneDX/cyclonedx-python/pull/877),
  [`3c86517`](https://github.com/CycloneDX/cyclonedx-python/commit/3c86517a9e9986270cf7d2c51a2d62957fbdb712))

- Showcase usage with `uv` ([#858](https://github.com/CycloneDX/cyclonedx-python/pull/858),
  [`efd45b1`](https://github.com/CycloneDX/cyclonedx-python/commit/efd45b1f6f4aaebf70a9d645636626636145de26))

### Features

- Deprecate CLI switch `--outfile`; use new `--output-file` instead
  ([#875](https://github.com/CycloneDX/cyclonedx-python/pull/875),
  [`fb30ee0`](https://github.com/CycloneDX/cyclonedx-python/commit/fb30ee098f10ba805212bb6463ec7933676592c1))

- Deprecate CLI switch `--schema-version`; use new `--spec-version` instead
  ([#871](https://github.com/CycloneDX/cyclonedx-python/pull/871),
  [`bbae05f`](https://github.com/CycloneDX/cyclonedx-python/commit/bbae05f3130c79c442f67f3ee544a7e4701d5a86))

- Support `cyclonedx-python-lib ^10`
  ([#880](https://github.com/CycloneDX/cyclonedx-python/pull/880),
  [`545dde0`](https://github.com/CycloneDX/cyclonedx-python/commit/545dde0cfd380748f711e159ecb2a7c4fb9cf81b))


## v5.3.0 (2025-02-26)

### Features

- Add support for `cyclonedx-python-lib>=9.0<10`
  ([#854](https://github.com/CycloneDX/cyclonedx-python/pull/854),
  [`45ae96e`](https://github.com/CycloneDX/cyclonedx-python/commit/45ae96eca790d68fc8262e70307110aab36c29c2))


## v5.2.0 (2025-02-20)

### Documentation

- Showcase `uv` as installation option
  ([#847](https://github.com/CycloneDX/cyclonedx-python/pull/847),
  [`12cc59b`](https://github.com/CycloneDX/cyclonedx-python/commit/12cc59bb0c38ae2ce72bc9e54c46762dafe399fc))

### Features

- Subcommand `environment` got aliases `env`, `venv`
  ([#850](https://github.com/CycloneDX/cyclonedx-python/pull/850),
  [`aaed12a`](https://github.com/CycloneDX/cyclonedx-python/commit/aaed12a74d68fe8d8eb2fadc7b8d226968f335cf))


## v5.1.2 (2025-01-21)

### Bug Fixes

- **poetry**: Properly handle multi-declaration (optional) dependencies
  ([#842](https://github.com/CycloneDX/cyclonedx-python/pull/842),
  [`18c5f0e`](https://github.com/CycloneDX/cyclonedx-python/commit/18c5f0ec8e4418aeaf7d6ee2e36b40133f9d0e5a))

### Documentation

- Add console classifier
  ([`75f640c`](https://github.com/CycloneDX/cyclonedx-python/commit/75f640cdede42676c0d9e96a359b111582596ff9))

- Fix typos in comments
  ([`8228cbb`](https://github.com/CycloneDX/cyclonedx-python/commit/8228cbb65070008279859579b6149e6f6e6f0404))


## v5.1.1 (2024-11-09)

### Bug Fixes

- Schema-invalid CycloneDX when running PEP639 analysis
  ([#828](https://github.com/CycloneDX/cyclonedx-python/pull/828),
  [`b2595cf`](https://github.com/CycloneDX/cyclonedx-python/commit/b2595cf829f57c0712394ae5f159af395b59c43e))

### Documentation

- Fix headline structure in readme
  ([`74f07e1`](https://github.com/CycloneDX/cyclonedx-python/commit/74f07e16871b9ee5f9f7581edffa3af76b2b7ba6))


## v5.1.0 (2024-10-23)

### Features

- Add Python 3.13 support ([#818](https://github.com/CycloneDX/cyclonedx-python/pull/818),
  [`f4eb79e`](https://github.com/CycloneDX/cyclonedx-python/commit/f4eb79e50bd5a1462c47ad259d632937d951bf96))


## v5.0.0 (2024-10-15)

### Documentation

- **chaneglog**: Omit chore/ci/refactor/style/test/build
  ([#813](https://github.com/CycloneDX/cyclonedx-python/pull/813),
  [`6707959`](https://github.com/CycloneDX/cyclonedx-python/commit/67079598b520fc7319f1c83ff562584f4acdd09c))

### Features

- V5.0.0 ([#797](https://github.com/CycloneDX/cyclonedx-python/pull/797),
  [`34cf6e3`](https://github.com/CycloneDX/cyclonedx-python/commit/34cf6e316f5f065b00cdebbed0791662500e6c4c))

### BREAKING Changes

* Emitted metadata tool name is `cyclonedx-py`, was `cyclonedx-bom`. * Emitted metadata tools are up
  to non-deprecated CycloneDX specification. * No longer emit deprecated or undocumented properties
  in namespace
  [`cdx:poetry`](https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/poetry.md)
  (see previous release 4.6.0 for official replacements). - `cdx:poetry:source:package:reference` -
  `cdx:poetry:package:source:resolved_reference` -
  `cdx:poetry:package:source:vcs:requested_revision` - `cdx:poetry:package:source:vcs:commit_id`

The mentioned changes are considered "breaking" for processes that relied on the respective data
  structures. Migration paths are self-explanatory.

### Dependencies

* Requires `cyclonedx-python-lib>=8.0.0,<9 ` now, was `>=7.3.0,<8.0.0,!=7.3.1`.

## v4.6.1 (2024-09-30)

### Bug Fixes

- Help page for sub command "environment" on windows
  ([#805](https://github.com/CycloneDX/cyclonedx-python/pull/805),
  [`9e8a5d7`](https://github.com/CycloneDX/cyclonedx-python/commit/9e8a5d72045b3477e5523ed891493c29a584f35f))

### Documentation

- Contrib and setup hint
  ([`2ae46ff`](https://github.com/CycloneDX/cyclonedx-python/commit/2ae46ff222067724d4f1e5e23335cd342f6775a6))


## v4.6.0 (2024-09-20)

### Documentation

- Reformat help page in `usage` docs
  ([#788](https://github.com/CycloneDX/cyclonedx-python/pull/788),
  [`a1354e5`](https://github.com/CycloneDX/cyclonedx-python/commit/a1354e5fd074036499d308488e0e621647afc3ce))

### Features

- Populate properties `cdx:python:package:source:vcs:...`
  ([#790](https://github.com/CycloneDX/cyclonedx-python/pull/790),
  [`b08e1bb`](https://github.com/CycloneDX/cyclonedx-python/commit/b08e1bb46871b167fb0ca135d2f97ad8a19df313))


## v4.5.1 (2024-09-18)

### Bug Fixes

- Assert copyright headers ([#787](https://github.com/CycloneDX/cyclonedx-python/pull/787),
  [`dddcb5d`](https://github.com/CycloneDX/cyclonedx-python/commit/dddcb5dc6529e60c82dcfd756a0a8b31ae76e9bf))

### Documentation

- Fix typo
  ([`9f9fa9e`](https://github.com/CycloneDX/cyclonedx-python/commit/9f9fa9e795b2aea847ae7639b018fd6c32d7e38c))


## v4.5.0 (2024-06-10)

### Documentation

- Exclude dep bumps from changelog ([#750](https://github.com/CycloneDX/cyclonedx-python/pull/750),
  [`3d02d6a`](https://github.com/CycloneDX/cyclonedx-python/commit/3d02d6ab32d864a6cf9c84a12f60623c6a784c4b))

- Ossf best practice badge percentage
  ([`5717803`](https://github.com/CycloneDX/cyclonedx-python/commit/5717803b27f71d6133cce5a5ea91cd87f130626a))

### Features

- Environment - gather declared license information according to PEP639
  ([#755](https://github.com/CycloneDX/cyclonedx-python/pull/755),
  [`e9cc805`](https://github.com/CycloneDX/cyclonedx-python/commit/e9cc8058bb299e98a6f645426a2626bcfa3f06eb))


## v4.4.3 (2024-04-26)

### Bug Fixes

- Do not use `cyclonedx-lib==7.3.1` ([#729](https://github.com/CycloneDX/cyclonedx-python/pull/729),
  [`aa715c0`](https://github.com/CycloneDX/cyclonedx-python/commit/aa715c0e94045c35fda7b6908c3c59cb84fb5e0c))


## v4.4.2 (2024-04-21)

### Bug Fixes

- Release `lates` container image ([#726](https://github.com/CycloneDX/cyclonedx-python/pull/726),
  [`0155450`](https://github.com/CycloneDX/cyclonedx-python/commit/015545014d7bb0fe72438d6707db4abc89dba031))


## v4.4.1 (2024-04-21)

### Bug Fixes

- Release `lates` container image ([#725](https://github.com/CycloneDX/cyclonedx-python/pull/725),
  [`8ba9d0b`](https://github.com/CycloneDX/cyclonedx-python/commit/8ba9d0b35f9d9593b5a3e232bf5e92d79b42fab9))


## v4.4.0 (2024-04-21)

### Features

- Publish to GHCR ([#724](https://github.com/CycloneDX/cyclonedx-python/pull/724),
  [`8c18484`](https://github.com/CycloneDX/cyclonedx-python/commit/8c184842af1a790692a898e9437a209a8fa65422))


## v4.3.0 (2024-04-20)

### Features

- Improve declared licenses detection
  ([#722](https://github.com/CycloneDX/cyclonedx-python/pull/722),
  [`b0ae453`](https://github.com/CycloneDX/cyclonedx-python/commit/b0ae453e7dc69356ba5e1b987a6b19a31d106909))


## v4.2.0 (2024-04-18)

### Features

- Support CycloneDX 1.6 output ([#720](https://github.com/CycloneDX/cyclonedx-python/pull/720),
  [`639b35a`](https://github.com/CycloneDX/cyclonedx-python/commit/639b35ad7e9aa832a4ad9b489a2391348f97fc15))


## v4.1.6 (2024-04-15)

### Bug Fixes

- More resilent PEP610 parsing ([#716](https://github.com/CycloneDX/cyclonedx-python/pull/716),
  [`93f0184`](https://github.com/CycloneDX/cyclonedx-python/commit/93f0184dd969db1536128d1ec4861f84977f0a91))


## v4.1.5 (2024-04-11)

### Bug Fixes

- Docs for default of CLI switch `--mc-type`
  ([#710](https://github.com/CycloneDX/cyclonedx-python/pull/710),
  [`a218b40`](https://github.com/CycloneDX/cyclonedx-python/commit/a218b40ae8bc383e449b69ba3aa5280253387f19))


## v4.1.4 (2024-03-28)

### Bug Fixes

- Poetry analyzer crashed with certain optional package's version constraints
  ([#703](https://github.com/CycloneDX/cyclonedx-python/pull/703),
  [`8ade6e1`](https://github.com/CycloneDX/cyclonedx-python/commit/8ade6e18637428e86332ecd1019416dfc121e862))


## v4.1.3 (2024-03-15)

### Bug Fixes

- Declared license texts as such, not as license name
  ([#694](https://github.com/CycloneDX/cyclonedx-python/pull/694),
  [`ec7ab3e`](https://github.com/CycloneDX/cyclonedx-python/commit/ec7ab3eb3a0aba31ce84227637aa0c91e05e76ba))

### Documentation

- Imprve `environment` use cases and examples
  ([#690](https://github.com/CycloneDX/cyclonedx-python/pull/690),
  [`0d38c7b`](https://github.com/CycloneDX/cyclonedx-python/commit/0d38c7b252e8d7f868656dd4663d1aac1c10fba5))


## v4.1.2 (2024-03-01)

### Build System

- Use poetry v1.8.1 ([#682](https://github.com/CycloneDX/cyclonedx-python/pull/682),
  [`dba63b8`](https://github.com/CycloneDX/cyclonedx-python/commit/dba63b8509336757d17d1cd21cdbe72517ecfd67))


## v4.1.1 (2024-02-03)

### Bug Fixes

- Normalize package extras ([#671](https://github.com/CycloneDX/cyclonedx-python/pull/671),
  [`4d550ad`](https://github.com/CycloneDX/cyclonedx-python/commit/4d550ad2467bcfbf3a8705188fd4f15e0dee194e))

### Documentation

- Improve example for programmatic call of CLI
  ([#670](https://github.com/CycloneDX/cyclonedx-python/pull/670),
  [`2ac3f21`](https://github.com/CycloneDX/cyclonedx-python/commit/2ac3f218840b256bc84f25fa962febf484800860))


## v4.1.0 (2024-02-02)

### Features

- Support poetry multi-constraint dependencies
  ([#668](https://github.com/CycloneDX/cyclonedx-python/pull/668),
  [`50d2a4b`](https://github.com/CycloneDX/cyclonedx-python/commit/50d2a4bb1827fc0e7de83a7f78fc0a4d278df93e))


## v4.0.0 (2024-01-31)

### Features

- V4.0.0 ([#605](https://github.com/CycloneDX/cyclonedx-python/pull/605),
  [`6d24e65`](https://github.com/CycloneDX/cyclonedx-python/commit/6d24e656835d1be2705237100b289ae0c3ff51df))

## Changelog

See also the migration guide in the docs.

- BC: Removed support for python < 3.8 
- BC: Removed deprecated shell script `cyclonedx-bom`; use
  `cyclonedx-py` instead 
- BC: Removed conda support. However, conda's Python environments are fully
  supported. See below. 
- BC: Removed public API. You may use the CLI instead, see chapter "usage"
  in the docs. 
- BC: Complete redesign of the CommandLineInterface(CLI): 
  - Uses sub-commands for
  easy accessibility and divide in specific purposes and domains 
  - Easy understandable flags,
  switches and options -- in accordance with the domains 
  - Updated help pages, added usage examples
  - Dozens of new features and fixes, such as: 
  - _environment_ analyzer supports any Python
  (virtual) environment -- including support for, but not limited to: _conda_, _Hatch_, _PDM_,
  _Pipenv_, _Poetry_, _venv_, _virtualenv_ 
  - _Poetry_ analyzer support groups, filtering, and such 
  - _Pipenv_ analyzer support categories, filtering, and such 
  - _requirements_ analyzer is feature
  complete and fixed - More details in the SBOM results (based on method) 
  - PackageURLs may have
  more qualifiers (enabled per default, disable via `--short-PURLs`) 
  - component properties
  according to [official
  taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/) - SBOM results
  may be validated (enabled per default, disable via `--no-validate`) 
  - SBOM results may have
  dependency graph populated (if supported by method - applies to _environment_ and _Poetry_) - SBOM
  results may have root-component populated (if `pyproject` provided) 
  - SBOM results are more
  `diff`-friendly and not just one long line of text 
  - Fixed possible issues with input data
  encoding 
  - May omit dev-dependencies or domain-specific groups/categories (if supported by method
  and issued by CLI switches) 
  - Strip authentication secrets from (private) download/index URLs 
  - Support CycloneDX 1.5 
  - which is the default now - Upgraded documentation, examples, ... 
  - Complete rewrite from scratch - Dependencies were bumped, dropped, added, ... 
  - QA and test suites
  were massively enhanced

## v3.11.7 (2023-11-03)

### Bug Fixes

- Toml-compatible fingers-crossed handling for failed input data decoding
  ([#613](https://github.com/CycloneDX/cyclonedx-python/pull/613),
  [`fb3d7bf`](https://github.com/CycloneDX/cyclonedx-python/commit/fb3d7bfd1216ad8b5328a1d348fea04fee31d3a4))


## v3.11.6 (2023-11-03)

### Bug Fixes

- Added a fingers-crossed handling for failed input data decoding
  ([#612](https://github.com/CycloneDX/cyclonedx-python/pull/612),
  [`be55902`](https://github.com/CycloneDX/cyclonedx-python/commit/be559020e482795c6603f36e98713c6f7bde1e34))


## v3.11.5 (2023-10-20)

### Bug Fixes

- Custom input encoding ([#601](https://github.com/CycloneDX/cyclonedx-python/pull/601),
  [`363934c`](https://github.com/CycloneDX/cyclonedx-python/commit/363934c0bc69ebbb23472f1173bf3c6b1e3c023a))


## v3.11.4 (2023-10-19)

### Bug Fixes

- Input file encoding fallback
  ([`0bc7296`](https://github.com/CycloneDX/cyclonedx-python/commit/0bc72964d0578f713f405bc101742ef096bf8fd7))


## v3.11.3 (2023-10-19)

### Bug Fixes

- Input file encoding ([#596](https://github.com/CycloneDX/cyclonedx-python/pull/596),
  [`a9dda4b`](https://github.com/CycloneDX/cyclonedx-python/commit/a9dda4bfd0e68529628eab99b6db00fb5214bfc3))

### Documentation

- Adjust syntax hilight for code blocks
  ([#592](https://github.com/CycloneDX/cyclonedx-python/pull/592),
  [`ccac31e`](https://github.com/CycloneDX/cyclonedx-python/commit/ccac31eb4d0996236da24ca9efb57af66bd1a020))

- Mark `ShellSession` in README
  ([`411cf3d`](https://github.com/CycloneDX/cyclonedx-python/commit/411cf3d0a4b5005c1591211ecdc464d4747d69f1))

- Publish coverage ([#600](https://github.com/CycloneDX/cyclonedx-python/pull/600),
  [`bd4f48e`](https://github.com/CycloneDX/cyclonedx-python/commit/bd4f48ef7f3c4c890a138c45dbc87f6ca3e2cf7b))


## v3.11.2 (2023-07-12)

### Bug Fixes

- Referenced branch `main`, instead of `master`
  ([#562](https://github.com/CycloneDX/cyclonedx-python/pull/562),
  [`830d15c`](https://github.com/CycloneDX/cyclonedx-python/commit/830d15c27fadb475fa9a15918b1d5930cd71834d))


## v3.11.1 (2023-07-12)

### Bug Fixes

- Fix typo in help page ([#552](https://github.com/CycloneDX/cyclonedx-python/pull/552),
  [`19bf41a`](https://github.com/CycloneDX/cyclonedx-python/commit/19bf41a52a698ee3ddee5fafc5d293ea3d9427be))


## v3.11.0 (2023-02-11)

### Documentation

- Fix shields ([#473](https://github.com/CycloneDX/cyclonedx-python/pull/473),
  [`e32b288`](https://github.com/CycloneDX/cyclonedx-python/commit/e32b28894a8859925f22a1f45aec8608e7cd8bc3))

- Fix typo in CLI help page ([#490](https://github.com/CycloneDX/cyclonedx-python/pull/490),
  [`a8a8445`](https://github.com/CycloneDX/cyclonedx-python/commit/a8a844504494d10c217ba4739e6ff09b4ca34f67))

- Fix typos ([#482](https://github.com/CycloneDX/cyclonedx-python/pull/482),
  [`edbe3d4`](https://github.com/CycloneDX/cyclonedx-python/commit/edbe3d4e0ee62396ac10b42dd9ee5d6094817675))

### Features

- Deprecated CLI command `cyclonedx-bom` prints deprecation warning on STDERR before execution
  ([#489](https://github.com/CycloneDX/cyclonedx-python/pull/489),
  [`2009236`](https://github.com/CycloneDX/cyclonedx-python/commit/2009236c537af212aab1d5907e02f2b003f3062c))


## v3.10.1 (2022-12-15)

### Bug Fixes

- Purl for PyPI packages from 'conda list' have the correct format now
  ([#471](https://github.com/CycloneDX/cyclonedx-python/pull/471),
  [`1573064`](https://github.com/CycloneDX/cyclonedx-python/commit/157306483a21583d752714a77ad7d0c7395291e5))

### Documentation

- Improve CONTRIBUTION instructions - sign-off step
  ([#470](https://github.com/CycloneDX/cyclonedx-python/pull/470),
  [`578c0a8`](https://github.com/CycloneDX/cyclonedx-python/commit/578c0a88e63c804b1462e3d3b617f56b53b6012e))


## v3.10.0 (2022-12-13)

### Features

- Add support for poetry lock format v2.0
  ([#469](https://github.com/CycloneDX/cyclonedx-python/pull/469),
  [`0b1e07f`](https://github.com/CycloneDX/cyclonedx-python/commit/0b1e07f91aada201088605a84ea394182ce0f10e))


## v3.9.0 (2022-12-13)

### Features

- Parsers can outbut more debug messages
  ([#466](https://github.com/CycloneDX/cyclonedx-python/pull/466),
  [`9eedb4f`](https://github.com/CycloneDX/cyclonedx-python/commit/9eedb4ff27bb81f4ad323e9fa0f79230b0710032))


## v3.8.0 (2022-12-12)

### Features

- Error- and debug-output is send to STDERR, instead of STDOUT
  ([#465](https://github.com/CycloneDX/cyclonedx-python/pull/465),
  [`f543b69`](https://github.com/CycloneDX/cyclonedx-python/commit/f543b69ee4463df3fb4d4b7c86475562f62e4744))


## v3.7.4 (2022-12-12)

### Bug Fixes

- Ignore broken licenses in env parser
  ([#463](https://github.com/CycloneDX/cyclonedx-python/pull/463),
  [`3118acd`](https://github.com/CycloneDX/cyclonedx-python/commit/3118acdf180b6d8d35a637b3e94dc6ec7c5c5b3d))


## v3.7.3 (2022-12-11)

### Bug Fixes

- Adjust dependency `pip-requirements-parser` to a working version
  ([#450](https://github.com/CycloneDX/cyclonedx-python/pull/450),
  [`6101986`](https://github.com/CycloneDX/cyclonedx-python/commit/610198659be408b5ef17d649aa381944d992a7dd))


## v3.7.2 (2022-11-15)

### Bug Fixes

- Add a missing space in the help pages `pathto` -> `path to`
  ([#443](https://github.com/CycloneDX/cyclonedx-python/pull/443),
  [`bc5fe57`](https://github.com/CycloneDX/cyclonedx-python/commit/bc5fe5760565e608387ad7638126869550d65213))

### Documentation

- Fix typo `pathto` -> `path to` ([#443](https://github.com/CycloneDX/cyclonedx-python/pull/443),
  [`bc5fe57`](https://github.com/CycloneDX/cyclonedx-python/commit/bc5fe5760565e608387ad7638126869550d65213))


## v3.7.1 (2022-11-10)

### Bug Fixes

- **EnvironmentParser**: Reduced crashes if no Classifiers are found
  ([#441](https://github.com/CycloneDX/cyclonedx-python/pull/441),
  [`67f56e7`](https://github.com/CycloneDX/cyclonedx-python/commit/67f56e7bfa4fb9d50654ebd07ece1ad14377a355))


## v3.7.0 (2022-11-10)

### Features

- Pass purl-bom-ref to EnvironmentParser
  ([#432](https://github.com/CycloneDX/cyclonedx-python/pull/432),
  [`7cfefeb`](https://github.com/CycloneDX/cyclonedx-python/commit/7cfefeb389b3c63b69ad93aeca1a709231da2901))


## v3.6.4 (2022-11-10)

### Bug Fixes

- **EnvironmentParser**: Remove code break when classifier parsing in py>=3.8
  ([#431](https://github.com/CycloneDX/cyclonedx-python/pull/431),
  [`4ab075e`](https://github.com/CycloneDX/cyclonedx-python/commit/4ab075ee814571a8dc8c1e7b962686b232619330))


## v3.6.3 (2022-09-19)

### Bug Fixes

- Ci release pipeline
  ([`99ccdc6`](https://github.com/CycloneDX/cyclonedx-python/commit/99ccdc671f5a7a941f31199813bce71405bbfdd8))


## v3.6.2 (2022-09-19)

### Bug Fixes

- Ci release pipeline
  ([`6515071`](https://github.com/CycloneDX/cyclonedx-python/commit/6515071fc95d2b460577d0fbceb7d6c34a18c508))


## v3.6.1 (2022-09-19)

### Bug Fixes

- Properly declare licenses from environment
  ([#417](https://github.com/CycloneDX/cyclonedx-python/pull/417),
  [`25f9e29`](https://github.com/CycloneDX/cyclonedx-python/commit/25f9e29a162f20918b6f1bbe887cc7b18c623c16))


## v3.6.0 (2022-09-16)

### Documentation

- Describe `cyclonedx-py` rather than `cyclonedx-bom`
  ([`c04196e`](https://github.com/CycloneDX/cyclonedx-python/commit/c04196e4404efc0513676e5baefeaf03e6b3b8e3))

- Fix minor typo in poetry usage docs
  ([#407](https://github.com/CycloneDX/cyclonedx-python/pull/407),
  [`0abe230`](https://github.com/CycloneDX/cyclonedx-python/commit/0abe23049b5423f55b3e0951a00047f4e3f93056))

- Minor updates to poetry usage details & contributing.md
  ([#407](https://github.com/CycloneDX/cyclonedx-python/pull/407),
  [`0abe230`](https://github.com/CycloneDX/cyclonedx-python/commit/0abe23049b5423f55b3e0951a00047f4e3f93056))

### Features

- Enable dependency `cyclonedx-python-lib@^3`
  ([#418](https://github.com/CycloneDX/cyclonedx-python/pull/418),
  [`05cd51e`](https://github.com/CycloneDX/cyclonedx-python/commit/05cd51e1da261d29fb5c3e1722544a8f00a0cfcd))


## v3.5.0 (2022-06-27)


## v3.4.0 (2022-06-16)


## v3.3.0 (2022-06-16)


## v3.2.2 (2022-06-02)

### Bug Fixes

- Add actively used (transitive) dependencies
  ([#363](https://github.com/CycloneDX/cyclonedx-python/pull/363),
  [`1f45ad9`](https://github.com/CycloneDX/cyclonedx-python/commit/1f45ad9162be511f07e9310414793218c554a097))


## v3.2.1 (2022-04-05)

### Bug Fixes

- Cli default file for json format
  ([`8747620`](https://github.com/CycloneDX/cyclonedx-python/commit/8747620dac7ed3eeff69369c05dfb6386a56e549))


## v3.2.0 (2022-04-05)

### Bug Fixes

- Fix style and remove unnecessary package
  ([#333](https://github.com/CycloneDX/cyclonedx-python/pull/333),
  [`0ff6493`](https://github.com/CycloneDX/cyclonedx-python/commit/0ff6493dd59d2e8efafd35d4460847525e590937))

### Documentation

- Describe methods to call the tool
  ([`2bac83a`](https://github.com/CycloneDX/cyclonedx-python/commit/2bac83a6c6f7354d8b7218c32b4b2e5d96b2fd0c))

### Features

- Make module callable
  ([`5b3d8d7`](https://github.com/CycloneDX/cyclonedx-python/commit/5b3d8d7641b0f2825e5419b5ad8c8a75bf66403b))


## v3.1.1 (2022-03-21)

### Bug Fixes

- **conda-parser**: Version recognition for strings
  ([#332](https://github.com/CycloneDX/cyclonedx-python/pull/332),
  [`65246dd`](https://github.com/CycloneDX/cyclonedx-python/commit/65246ddfa9a55ce53fbf87f33b1f269c519f9b3a))

### Documentation

- Add hint for RTFD to README
  ([`cf4f534`](https://github.com/CycloneDX/cyclonedx-python/commit/cf4f534401dc90dbe093ce1a094efb02e5fb7c90))

- Add link to https://cyclonedx.org/ to README
  ([`fc4b8e4`](https://github.com/CycloneDX/cyclonedx-python/commit/fc4b8e44bec39b175bb8994e0a59bc5076d1b2a6))

- Add RTFD shield to README
  ([`7fef6ee`](https://github.com/CycloneDX/cyclonedx-python/commit/7fef6eec5d553c7687e7b2d2af1ba4e330f16490))

- Fixed link to RTFD
  ([`3a8669a`](https://github.com/CycloneDX/cyclonedx-python/commit/3a8669ad7ba4230d06d1e0965342a5a836a52d1f))


## v3.1.0 (2022-03-10)

### Bug Fixes

- Sort imports
  ([`fdec44b`](https://github.com/CycloneDX/cyclonedx-python/commit/fdec44bc111d7eb1add080a219dbc77744678f8a))

- Try to fix the temp file issue on Windows machines
  ([`684d4f0`](https://github.com/CycloneDX/cyclonedx-python/commit/684d4f03ad6f8c0764dfaf8f3a38a09b91b69e5d))

### Documentation

- Update RequirementsFileParser docs to include nested file support
  ([`9e9021d`](https://github.com/CycloneDX/cyclonedx-python/commit/9e9021decb19d8262e87fe6955577c1bd1309d95))

### Features

- Add pip-requirements-parser and update virtualenv to latest version
  ([`73b2182`](https://github.com/CycloneDX/cyclonedx-python/commit/73b2182550d9635a0a5ab8e4f2226f37cf6b1b35))

- Add support for hashes, local packages and private repositories
  ([`addc21a`](https://github.com/CycloneDX/cyclonedx-python/commit/addc21ae832f642298f665d426c576822038fb2f))


## v3.0.0 (2022-02-21)

### Features

- Added marker and classifiers to denote this as typed
  ([#313](https://github.com/CycloneDX/cyclonedx-python/pull/313),
  [`f317353`](https://github.com/CycloneDX/cyclonedx-python/commit/f317353bd7a24dbf4fb31642d766d94da609eb42))

- Bump to latest `cyclonedx-python-lib`
  ([`5902fbf`](https://github.com/CycloneDX/cyclonedx-python/commit/5902fbf9dc5becdf7d92180242488e56b998d9de))

BREAKING CHANGE: Default Schema Version has been replaced by notion of LATEST supported Schema
  Version

- Update to latest RC of `cyclonedx-python-lib`
  ([`6c8b517`](https://github.com/CycloneDX/cyclonedx-python/commit/6c8b5173f07329b2086312d27af5d111f9b2c7ed))

- Update to latest RC of `cyclonedx-python-lib`
  ([`bc8ee6b`](https://github.com/CycloneDX/cyclonedx-python/commit/bc8ee6bb115dd5214358430f64bd0581de5cb2e4))

### Breaking Changes

- Default Schema Version has been replaced by notion of LATEST supported Schema Version


## v2.0.3 (2022-02-03)

### Bug Fixes

- Docker image releae checkout ref w/o `tags`
  ([#309](https://github.com/CycloneDX/cyclonedx-python/pull/309),
  [`5d8b1e1`](https://github.com/CycloneDX/cyclonedx-python/commit/5d8b1e159c2ced59e810b9e9564e19a29fe263d0))


## v2.0.2 (2022-02-03)

### Bug Fixes

- Properly support reading from stdin
  ([#307](https://github.com/CycloneDX/cyclonedx-python/pull/307),
  [`23f31a0`](https://github.com/CycloneDX/cyclonedx-python/commit/23f31a03a4fbf888f396b88a9413c054358b2a3a))


## v2.0.1 (2022-01-24)

### Bug Fixes

- Bump dependencies to get latest `cyclonedx-python-lib`
  ([`87c3fe7`](https://github.com/CycloneDX/cyclonedx-python/commit/87c3fe7747cd8abd55ad5699bfc87ad9877c8132))


## v2.0.0 (2022-01-13)

### Bug Fixes

- Addressed flake8 issues ([#294](https://github.com/CycloneDX/cyclonedx-python/pull/294),
  [`7bb6d32`](https://github.com/CycloneDX/cyclonedx-python/commit/7bb6d328adec59cdd4c3ab80eb5f39568ca3bc9c))

- Corrected import ([#294](https://github.com/CycloneDX/cyclonedx-python/pull/294),
  [`7bb6d32`](https://github.com/CycloneDX/cyclonedx-python/commit/7bb6d328adec59cdd4c3ab80eb5f39568ca3bc9c))

### Documentation

- Readme maintenance - shields & links
  ([#266](https://github.com/CycloneDX/cyclonedx-python/pull/266),
  [`a34046f`](https://github.com/CycloneDX/cyclonedx-python/commit/a34046f9b4c96d013fdf2dbdac5e930aa9204e15))

### Features

- Add support for CycloneDX 1.4 specification
  ([#294](https://github.com/CycloneDX/cyclonedx-python/pull/294),
  [`7bb6d32`](https://github.com/CycloneDX/cyclonedx-python/commit/7bb6d328adec59cdd4c3ab80eb5f39568ca3bc9c))

- Add support for output to CycloneDX 1.4 (draft)
  ([#294](https://github.com/CycloneDX/cyclonedx-python/pull/294),
  [`7bb6d32`](https://github.com/CycloneDX/cyclonedx-python/commit/7bb6d328adec59cdd4c3ab80eb5f39568ca3bc9c))

- Breaking CHANGE - relocated concrete parsers
  ([#294](https://github.com/CycloneDX/cyclonedx-python/pull/294),
  [`7bb6d32`](https://github.com/CycloneDX/cyclonedx-python/commit/7bb6d328adec59cdd4c3ab80eb5f39568ca3bc9c))

- Breaking CHANGE - relocated concrete parsers from `cyclonedx-python-lib`
  ([#294](https://github.com/CycloneDX/cyclonedx-python/pull/294),
  [`7bb6d32`](https://github.com/CycloneDX/cyclonedx-python/commit/7bb6d328adec59cdd4c3ab80eb5f39568ca3bc9c))


## v1.5.3 (2021-11-23)


## v1.5.2 (2021-11-23)

### Bug Fixes

- Corrected docker image build process to not rely on `dist` folder which is cleaned up by
  python-semantic-release
  ([`6c65c11`](https://github.com/CycloneDX/cyclonedx-python/commit/6c65c11d439169417e2ef7e94cacb1ec216eb11c))

- Revert to previous process for building Docker image as PyPi index update is too slow to pull
  straight away after publish
  ([`67bb738`](https://github.com/CycloneDX/cyclonedx-python/commit/67bb738246bfe0ca3acd409d8c5a27fd7a305347))


## v1.5.1 (2021-11-23)

### Bug Fixes

- Re-enable build and publish of Docker Image
  ([#263](https://github.com/CycloneDX/cyclonedx-python/pull/263),
  [`478360d`](https://github.com/CycloneDX/cyclonedx-python/commit/478360db0de269159ab6e3777cd291b87e2e1174))

- Update `Dockerfile` to use Python 3.10
  ([#263](https://github.com/CycloneDX/cyclonedx-python/pull/263),
  [`478360d`](https://github.com/CycloneDX/cyclonedx-python/commit/478360db0de269159ab6e3777cd291b87e2e1174))


## v1.5.0 (2021-11-17)

### Features

- Support for Python 3.10 ([#261](https://github.com/CycloneDX/cyclonedx-python/pull/261),
  [`f4f9ffe`](https://github.com/CycloneDX/cyclonedx-python/commit/f4f9ffe4b1e2d4fffe4ad0b274a067a20c9c372f))


## v1.4.3 (2021-11-16)

### Bug Fixes

- Add static code analysis, better typing and bump cyclonedx-python-lib to 0.11
  ([`d5d9f56`](https://github.com/CycloneDX/cyclonedx-python/commit/d5d9f563f2ceb1bdfb2f9cb39ff07af9f0deca26))


## v1.4.2 (2021-11-12)

### Bug Fixes

- If no input file is supplied and no input is provided on STDIN, we will now try to automatically
  locate (in the current working directory) a manifest with default name for the input type
  specified. This works for PIP (Pipfile.lock), Poetry (poetry.lock) and Requirements
  (requirements.txt)
  ([`93f9e59`](https://github.com/CycloneDX/cyclonedx-python/commit/93f9e5985f0d0cecd865b66119276d33b2175fe9))


## v1.4.1 (2021-10-26)

### Bug Fixes

- Corrected documentation after deprecation of `-rf`, `-pf`, `--poetry-file`, `--requirements-file`
  and `--pip-file`
  ([`4c4c8d8`](https://github.com/CycloneDX/cyclonedx-python/commit/4c4c8d8d4756ebc953c26504052d5469f3c47cfa))


## v1.4.0 (2021-10-21)

### Bug Fixes

- Encoding issues on Windows (bump cyclonedx-python-lib to ^0.10.1)
  ([`fe5df36`](https://github.com/CycloneDX/cyclonedx-python/commit/fe5df3607157b2f24854ef1f69457f163d79a093))

- Encoding issues on Windows (bump cyclonedx-python-lib to ^0.10.2)
  ([`da6772b`](https://github.com/CycloneDX/cyclonedx-python/commit/da6772be89ad923b1d8df6dd3b2a89c6e5805571))

### Features

- Add conda support (bump cyclonedx-python-lib to ^0.10.0)
  ([`cb24275`](https://github.com/CycloneDX/cyclonedx-python/commit/cb24275f3e8716244de2b4ef0a046b879fa88ba5))


## v1.3.1 (2021-10-19)

### Bug Fixes

- Bump to cyclonedx-python-lib to resolve issue #244
  ([`ebea3ef`](https://github.com/CycloneDX/cyclonedx-python/commit/ebea3ef47e917479a7474489bb274b5fa9704375))


## v1.3.0 (2021-10-19)

### Features

- Add license information in CycloneDX BOM when using Environment as the source
  ([`5d1f9a7`](https://github.com/CycloneDX/cyclonedx-python/commit/5d1f9a76cfa2bc1461a3dcf4c140d81876a37c40))


## v1.2.0 (2021-10-12)

### Features

- Update to latest stable cyclonedx-python-lib
  ([`6145bd5`](https://github.com/CycloneDX/cyclonedx-python/commit/6145bd52c450e66f42367e61e086d2a9d9818b47))


## v1.1.0 (2021-10-04)

### Features

- Add support for generating SBOM from poetry.lock files
  ([`bb4ac0f`](https://github.com/CycloneDX/cyclonedx-python/commit/bb4ac0f29b46db59b192191f65dfa40757268188))


## v1.0.5 (2021-09-27)

### Bug Fixes

- Handle `requirements.txt` which contain dependencies without a version statement and warn that
  they cannot be included in the resulting CycloneDX BOM
  ([`e637e56`](https://github.com/CycloneDX/cyclonedx-python/commit/e637e56cada6d841dae193c106647b0b03a4e776))


## v1.0.4 (2021-09-27)

### Bug Fixes

- Error message when `requirements.txt` file is non-existent updated
  ([`3bbc071`](https://github.com/CycloneDX/cyclonedx-python/commit/3bbc071a1ff26599bd9eb3220de38bd9c58fa294))


## v1.0.3 (2021-09-27)

### Bug Fixes

- Default to "requirements.txt" in current directory when "-r" flag is supplied but not "-rf" flag
  is supplied
  ([`bb7e30a`](https://github.com/CycloneDX/cyclonedx-python/commit/bb7e30a869300b1e63a00d7db4bcc7f35d68552d))

### Build System

- Added flake8 as dev dependency
  ([`a8fed84`](https://github.com/CycloneDX/cyclonedx-python/commit/a8fed843986d60da49649e6d9393ef77be2e80fa))

- Updated all dependencies
  ([`616b949`](https://github.com/CycloneDX/cyclonedx-python/commit/616b949e0d3200cd7c3a3e5131213e2e9bb51cfe))


## v1.0.2 (2021-09-13)

### Bug Fixes

- Release GH action
  ([`148421b`](https://github.com/CycloneDX/cyclonedx-python/commit/148421bcd8cea2b5f8f3bd5958f6f7171afe859e))


## v1.0.1 (2021-09-13)

### Bug Fixes

- **ci**: Corrected main to master branch.
  ([`7162cd9`](https://github.com/CycloneDX/cyclonedx-python/commit/7162cd9385729dafbdc15dbb55e9ac5adf3906cf))


## v0.4.3 (2020-12-06)


## v0.4.2 (2020-10-08)


## v0.4.1 (2020-09-09)


## v0.4.0 (2020-09-03)


## v0.3.5 (2019-12-04)


## v0.3.4 (2019-12-04)


## v0.3.3 (2019-11-13)

- Initial Release
