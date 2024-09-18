# CHANGELOG



## v4.5.1 (2024-09-18)

### Documentation

* docs: fix typo

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`9f9fa9e`](https://github.com/CycloneDX/cyclonedx-python/commit/9f9fa9e795b2aea847ae7639b018fd6c32d7e38c))

### Fix

* fix: assert copyright headers (#787)

utilizes flake8 plugin
&lt;https://pypi.org/project/flake8-copyright-validator/&gt; to assert the
correct headers

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`dddcb5d`](https://github.com/CycloneDX/cyclonedx-python/commit/dddcb5dc6529e60c82dcfd756a0a8b31ae76e9bf))


## v4.5.0 (2024-06-10)

### Chore

* chore: shield_ossf-best-practices subbary

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`1a1ad60`](https://github.com/CycloneDX/cyclonedx-python/commit/1a1ad606af261fc0e13095306571b2073ad4b3c3))

### Ci

* ci: modernize artifact action (#737)

supersedes #625 
supersedes #624

---------

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`1222201`](https://github.com/CycloneDX/cyclonedx-python/commit/122220199bf1185c2c607c2c9774e4f39427e866))

### Documentation

* docs: exclude dep bumps from changelog (#750)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3d02d6a`](https://github.com/CycloneDX/cyclonedx-python/commit/3d02d6ab32d864a6cf9c84a12f60623c6a784c4b))

* docs: OSSF best practice badge percentage

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`5717803`](https://github.com/CycloneDX/cyclonedx-python/commit/5717803b27f71d6133cce5a5ea91cd87f130626a))

### Feature

* feat: environment - gather declared license information according to PEP639 (#755)

From python environments, gather additional declared license information
according to [PEP 639](https://peps.python.org/pep-0639) (improving
license clarity with better package metadata).

New CLI switches for `cyclonedx environment`: 
* `--PEP-639`: Enable license gathering according to PEP 639 (improving
license clarity with better package metadata).
  The behavior may change during the draft development of the PEP.
* `--gather-license-texts`: Enable license text gathering.

In current state of implementation, `--gather-license-texts` has effect
only if `--PEP-639` is also given.



---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`e9cc805`](https://github.com/CycloneDX/cyclonedx-python/commit/e9cc8058bb299e98a6f645426a2626bcfa3f06eb))

### Refactor

* refactor: const for purl type `pypi` (#754)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`cba521e`](https://github.com/CycloneDX/cyclonedx-python/commit/cba521ee01aeb7bd3309518b4f46ba71d74abac9))

* refactor: `extred` -&gt; `extref` (#753)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a178d2e`](https://github.com/CycloneDX/cyclonedx-python/commit/a178d2ec62e2af7afab05a9807cc24102ff51a19))

### Unknown

* Create config.yml

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@owasp.org&gt; ([`f13311b`](https://github.com/CycloneDX/cyclonedx-python/commit/f13311bc691cd494636684a502760b5929cec3fb))

* Rename feature_request.md to 1-feature_request.md

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@owasp.org&gt; ([`c4b15d8`](https://github.com/CycloneDX/cyclonedx-python/commit/c4b15d82b5146d78edd87be2d799ec9be38df6f1))

* Rename bug_report.md to 2-bug_report.md

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@owasp.org&gt; ([`58199a5`](https://github.com/CycloneDX/cyclonedx-python/commit/58199a5c1bdc7fa9092a97a2bd24256e6b79de42))


## v4.4.3 (2024-04-26)

### Fix

* fix: do not use `cyclonedx-lib==7.3.1`  (#729)

add regression test for #727 
fixes #727

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`aa715c0`](https://github.com/CycloneDX/cyclonedx-python/commit/aa715c0e94045c35fda7b6908c3c59cb84fb5e0c))


## v4.4.2 (2024-04-21)

### Fix

* fix: release `lates` container image (#726)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`0155450`](https://github.com/CycloneDX/cyclonedx-python/commit/015545014d7bb0fe72438d6707db4abc89dba031))


## v4.4.1 (2024-04-21)

### Fix

* fix: release `lates` container image (#725)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`8ba9d0b`](https://github.com/CycloneDX/cyclonedx-python/commit/8ba9d0b35f9d9593b5a3e232bf5e92d79b42fab9))


## v4.4.0 (2024-04-21)

### Chore

* chore: semantic-release git commit/sign valid email address

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`692b8ea`](https://github.com/CycloneDX/cyclonedx-python/commit/692b8eaa0aecf7821e829edd6324cf33f07a86b7))

### Feature

* feat: publish to GHCR (#724)

Tee container image version of the app is also available on GitHubContainerRegistry: &lt;https://github.com/orgs/CycloneDX/packages/container/package/cyclonedx-python&gt;

---------


Signed-off-by: jxdv &lt;virgoj@protonmail.com&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Signed-off-by: semantic-release &lt;semantic-release@bot.local&gt;
Co-authored-by: jxdv &lt;virgoj@protonmail.com&gt;
Co-authored-by: semantic-release &lt;semantic-release@bot.local&gt; ([`8c18484`](https://github.com/CycloneDX/cyclonedx-python/commit/8c184842af1a790692a898e9437a209a8fa65422))


## v4.3.0 (2024-04-20)

### Feature

* feat: improve declared licenses detection (#722)

- Add declared licenses from License Troves if not mapped to SPDX
license ID
- CycloneDX 1.6 mark licenses as &#34;declared&#34;

fixes #718

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b0ae453`](https://github.com/CycloneDX/cyclonedx-python/commit/b0ae453e7dc69356ba5e1b987a6b19a31d106909))


## v4.2.0 (2024-04-18)

### Feature

* feat: support CycloneDX 1.6 output (#720)


Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`639b35a`](https://github.com/CycloneDX/cyclonedx-python/commit/639b35ad7e9aa832a4ad9b489a2391348f97fc15))


## v4.1.6 (2024-04-15)

### Fix

* fix: more resilent PEP610 parsing (#716)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`93f0184`](https://github.com/CycloneDX/cyclonedx-python/commit/93f0184dd969db1536128d1ec4861f84977f0a91))


## v4.1.5 (2024-04-11)

### Fix

* fix: docs for default of CLI switch `--mc-type` (#710)



Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a218b40`](https://github.com/CycloneDX/cyclonedx-python/commit/a218b40ae8bc383e449b69ba3aa5280253387f19))


## v4.1.4 (2024-03-28)

### Fix

* fix: poetry analyzer crashed with certain optional package&#39;s version constraints (#703)



Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`8ade6e1`](https://github.com/CycloneDX/cyclonedx-python/commit/8ade6e18637428e86332ecd1019416dfc121e862))


## v4.1.3 (2024-03-15)

### Ci

* ci: default to python 3.12 (#693)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`dc81c35`](https://github.com/CycloneDX/cyclonedx-python/commit/dc81c35e3389906ef1fe6944ee720b17c47a19e7))

### Documentation

* docs: imprve `environment` use cases and examples (#690)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`0d38c7b`](https://github.com/CycloneDX/cyclonedx-python/commit/0d38c7b252e8d7f868656dd4663d1aac1c10fba5))

### Fix

* fix: declared license texts as such, not as license name (#694)


Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`ec7ab3e`](https://github.com/CycloneDX/cyclonedx-python/commit/ec7ab3eb3a0aba31ce84227637aa0c91e05e76ba))


## v4.1.2 (2024-03-01)

### Build

* build: use poetry v1.8.1 (#682)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`dba63b8`](https://github.com/CycloneDX/cyclonedx-python/commit/dba63b8509336757d17d1cd21cdbe72517ecfd67))


## v4.1.1 (2024-02-03)

### Documentation

* docs: improve example for programmatic call of CLI (#670)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`2ac3f21`](https://github.com/CycloneDX/cyclonedx-python/commit/2ac3f218840b256bc84f25fa962febf484800860))

### Fix

* fix: normalize package extras (#671)

ALL names of package extras are normalized,  according to spec &lt;https://packaging.python.org/en/latest/specifications/name-normalization/#name-normalization&gt;

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`4d550ad`](https://github.com/CycloneDX/cyclonedx-python/commit/4d550ad2467bcfbf3a8705188fd4f15e0dee194e))


## v4.1.0 (2024-02-02)

### Feature

* feat: support poetry multi-constraint dependencies (#668)


Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`50d2a4b`](https://github.com/CycloneDX/cyclonedx-python/commit/50d2a4bb1827fc0e7de83a7f78fc0a4d278df93e))

### Unknown

* tests: modernize testbeds (#667)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`2fd3faf`](https://github.com/CycloneDX/cyclonedx-python/commit/2fd3faf45a5d3b9024bbf47d6e50c995880e2fd4))

* docs (#666)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`491e875`](https://github.com/CycloneDX/cyclonedx-python/commit/491e87564d124ccc91e21772423a10434ba5ff28))


## v4.0.0 (2024-01-31)

### Breaking

* feat!: v4.0.0  (#605)



  ## Changelog

  See also the migration guide in the docs.

  - BC: Removed support for python &lt; 3.8
  - BC: Removed deprecated shell script `cyclonedx-bom`; use `cyclonedx-py` instead
  - BC: Removed conda support. However, conda&#39;s Python environments are fully supported. See below.
  - BC: Removed public API. You may use the CLI instead, see chapter &#34;usage&#34; in the docs.
  - BC: Complete redesign of the CommandLineInterface(CLI):
    - Uses sub-commands for easy accessibility and divide in specific purposes and domains
    - Easy understandable flags, switches and options -- in accordance with the domains
    - Updated help pages, added usage examples 
  - Dozens of new features and fixes, such as:
    - _environment_ analyzer supports any Python (virtual) environment --
      including support for, but not limited to: _conda_, _Hatch_, _PDM_, _Pipenv_, _Poetry_, _venv_, _virtualenv_
    - _Poetry_ analyzer support groups, filtering, and such
    - _Pipenv_ analyzer support categories, filtering, and such
    - _requirements_ analyzer is feature complete and fixed
    - More details in the SBOM results (based on method)
    - PackageURLs may have more qualifiers (enabled per default, disable via `--short-PURLs`)
    - component properties according to [official taxonomy](https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/)
    - SBOM results may be validated (enabled per default, disable via `--no-validate`)
    - SBOM results may have dependency graph populated (if supported by method - applies to _environment_ and _Poetry_)
    - SBOM results may have root-component populated (if `pyproject` provided)
    - SBOM results are more `diff`-friendly and not just one long line of text
    - Fixed possible issues with input data encoding
    - May omit dev-dependencies or domain-specific groups/categories (if supported by method and issued by CLI switches)
    - Strip authentication secrets from (private) download/index URLs
    - Support CycloneDX 1.5 - which is the default now
  - Upgraded documentation, examples, ...
  - Complete rewrite from scratch
  - Dependencies were bumped, dropped, added, ...
  - QA and test suites were massively enhanced



---------

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;
Signed-off-by: Thomas Graf &lt;thomas.graf@siemens.com&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Signed-off-by: Andreas Fehlner &lt;fehlner@arcor.de&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@owasp.org&gt;
Signed-off-by: semantic-release &lt;semantic-release&gt;
Co-authored-by: Paul Horton &lt;paul.horton@owasp.org&gt;
Co-authored-by: Thomas Graf &lt;thomas.graf@siemens.com&gt;
Co-authored-by: semantic-release &lt;semantic-release&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt;
Co-authored-by: github-actions &lt;github-actions@github.com&gt;
Co-authored-by: Andreas Fehlner &lt;fehlner@arcor.de&gt; ([`6d24e65`](https://github.com/CycloneDX/cyclonedx-python/commit/6d24e656835d1be2705237100b289ae0c3ff51df))


## v3.11.7 (2023-11-03)

### Fix

* fix: toml-compatible fingers-crossed handling for failed input data decoding (#613)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`fb3d7bf`](https://github.com/CycloneDX/cyclonedx-python/commit/fb3d7bfd1216ad8b5328a1d348fea04fee31d3a4))

### Unknown

* 3.11.7

Automatically generated by python-semantic-release ([`f680a9a`](https://github.com/CycloneDX/cyclonedx-python/commit/f680a9a0d1b56f14c416f45877207ab1838f1c1c))


## v3.11.6 (2023-11-03)

### Fix

* fix: added a fingers-crossed handling for failed input data decoding (#612)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`be55902`](https://github.com/CycloneDX/cyclonedx-python/commit/be559020e482795c6603f36e98713c6f7bde1e34))

### Unknown

* 3.11.6

Automatically generated by python-semantic-release ([`6002e0e`](https://github.com/CycloneDX/cyclonedx-python/commit/6002e0ee2e74f1157718500a23a3d2236eb91919))


## v3.11.5 (2023-10-20)

### Fix

* fix: Custom input encoding (#601)

The custom input specified via CLI&#39;s `-i` option did not properly detect the input encoding.  
This was fixed.

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`363934c`](https://github.com/CycloneDX/cyclonedx-python/commit/363934c0bc69ebbb23472f1173bf3c6b1e3c023a))

### Unknown

* 3.11.5

Automatically generated by python-semantic-release ([`46cd517`](https://github.com/CycloneDX/cyclonedx-python/commit/46cd51753ab4746396d4c3d298292d6d3bf25056))


## v3.11.4 (2023-10-19)

### Fix

* fix: Input file encoding fallback

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`0bc7296`](https://github.com/CycloneDX/cyclonedx-python/commit/0bc72964d0578f713f405bc101742ef096bf8fd7))

### Unknown

* 3.11.4

Automatically generated by python-semantic-release ([`70889be`](https://github.com/CycloneDX/cyclonedx-python/commit/70889bedfcc10635b487a9a677316aab263c2184))


## v3.11.3 (2023-10-19)

### Chore

* chore: Update CONTRIBUTING.md

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@owasp.org&gt; ([`4adab1c`](https://github.com/CycloneDX/cyclonedx-python/commit/4adab1c4b5d79416db6fa6b24928ec7358ad4268))

### Documentation

* docs: publish coverage (#600)



Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`bd4f48e`](https://github.com/CycloneDX/cyclonedx-python/commit/bd4f48ef7f3c4c890a138c45dbc87f6ca3e2cf7b))

* docs: adjust syntax hilight for code blocks (#592)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`ccac31e`](https://github.com/CycloneDX/cyclonedx-python/commit/ccac31eb4d0996236da24ca9efb57af66bd1a020))

* docs: mark `ShellSession` in README

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`411cf3d`](https://github.com/CycloneDX/cyclonedx-python/commit/411cf3d0a4b5005c1591211ecdc464d4747d69f1))

### Fix

* fix: input file encoding (#596)

Input files in lock-format are expected in a certain encoding,
other input file encodings are detected.

fixes https://github.com/CycloneDX/cyclonedx-python/issues/448

---------

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a9dda4b`](https://github.com/CycloneDX/cyclonedx-python/commit/a9dda4bfd0e68529628eab99b6db00fb5214bfc3))

### Unknown

* 3.11.3

Automatically generated by python-semantic-release ([`02ab8cb`](https://github.com/CycloneDX/cyclonedx-python/commit/02ab8cbcf4bb495dbfc4e6e4ba5743f312d2abb0))

* Update usage.rst (#572)

Signed-off-by: Andreas Fehlner &lt;fehlner@arcor.de&gt; ([`04e1ea8`](https://github.com/CycloneDX/cyclonedx-python/commit/04e1ea8af23c55940c77ca8ab4af53bfa3f93647))


## v3.11.2 (2023-07-12)

### Fix

* fix: referenced branch `main`, instead of `master` (#562)

somebody renamed the `master` branch to `main`.
but forgot to transition the docs.

fixed this

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`830d15c`](https://github.com/CycloneDX/cyclonedx-python/commit/830d15c27fadb475fa9a15918b1d5930cd71834d))

### Unknown

* 3.11.2

Automatically generated by python-semantic-release ([`614f6fa`](https://github.com/CycloneDX/cyclonedx-python/commit/614f6fa0994132170bb8911dcd2eccdaed288ec0))


## v3.11.1 (2023-07-12)

### Chore

* chore: finish transition to main branch (#561)

somebody renamed the `master` branch to `main`.
but forgot to transition the CI triggers.

fixed this

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`ea233cb`](https://github.com/CycloneDX/cyclonedx-python/commit/ea233cbfced743859842336bfcc0cdd07ad3a7da))

* chore: rename file for lowest constraints/requirements (#517)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b4f0403`](https://github.com/CycloneDX/cyclonedx-python/commit/b4f04033452403dd3bf75d3ead034b7c2a92ae8e))

* chore: rename file for lowest constraints/requirements (#516)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a262bdb`](https://github.com/CycloneDX/cyclonedx-python/commit/a262bdb4a1e2692872d6b31ecf694c3cf6f0616f))

* chore: rename file for lowest constraints/requirements (#515)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a096cc7`](https://github.com/CycloneDX/cyclonedx-python/commit/a096cc7c1e890ef87005ccf271bcf5da5093240a))

* chore: rename file for lowest constraints/requirements (#514)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`02d8437`](https://github.com/CycloneDX/cyclonedx-python/commit/02d8437bbddf8e02727368abdfb80a7b5313d210))

* chore: adjust lowest constraints/requirements (#513)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`c8e6d0d`](https://github.com/CycloneDX/cyclonedx-python/commit/c8e6d0d3f25c8acc1f74b498bfaaf814885da48a))

### Ci

* ci: finish transition to main branch (#560)

somebody renamed the `master` branch to `main`.
but forgot to transition the CI triggers.

fixed this

followup of #558

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`0ea56c7`](https://github.com/CycloneDX/cyclonedx-python/commit/0ea56c764870240a5636be2ca2ec16ae2e342e43))

* ci: adjust release concurrecncy (#559)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`4b0ceac`](https://github.com/CycloneDX/cyclonedx-python/commit/4b0ceac138d309e2b0e4a516161ca3f5b9567c1a))

* ci: finish transition to main branch (#558)

somebody renamed the `master` branch to `main`.
but forgot to transition the CI triggers.

fixed this

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`7556eb9`](https://github.com/CycloneDX/cyclonedx-python/commit/7556eb98e4e985304a8afd876c8dd2c79f62d298))

* ci: add build concurrency (#557)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`fbcde26`](https://github.com/CycloneDX/cyclonedx-python/commit/fbcde26d392a5e3ab463ea92b602ba09d0f941ec))

* ci: disable tests on windows with py&gt;=3.8 (#556)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`c95e384`](https://github.com/CycloneDX/cyclonedx-python/commit/c95e384e3f071d6370440410f0d4944c969922ca))

### Fix

* fix: fix typo in help page (#552)

`it&#39;s` -&gt; `its`

fixes #551

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`19bf41a`](https://github.com/CycloneDX/cyclonedx-python/commit/19bf41a52a698ee3ddee5fafc5d293ea3d9427be))

### Unknown

* 3.11.1

Automatically generated by python-semantic-release ([`d90b45c`](https://github.com/CycloneDX/cyclonedx-python/commit/d90b45c4d11abe2c5abab794005a7565b8c3cf12))


## v3.11.0 (2023-02-11)

### Chore

* chore: fix lowest requirements for tests (#499)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`4928515`](https://github.com/CycloneDX/cyclonedx-python/commit/492851592fe8c130a3e55fe79c46bdf1d0def7bc))

* chore: add Paul Horton &amp; Jan Kowalleck as a maintainer

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b1a52fc`](https://github.com/CycloneDX/cyclonedx-python/commit/b1a52fc297f0ee774e77ceff47b99d780a4cc58c))

* chore: editorconfig

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`2122dba`](https://github.com/CycloneDX/cyclonedx-python/commit/2122dba8fada2336f7fd07dff33321dea165858b))

### Documentation

* docs: fix typo in CLI help page (#490) ([`a8a8445`](https://github.com/CycloneDX/cyclonedx-python/commit/a8a844504494d10c217ba4739e6ff09b4ca34f67))

* docs: fix typos (#482)

* Fix typo

Signed-off-by: Thomas Beutlich &lt;thomas.beutlich@neocx.de&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`edbe3d4`](https://github.com/CycloneDX/cyclonedx-python/commit/edbe3d4e0ee62396ac10b42dd9ee5d6094817675))

* docs: fix shields (#473)

caused by https://github.com/badges/shields/issues/8671

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`e32b288`](https://github.com/CycloneDX/cyclonedx-python/commit/e32b28894a8859925f22a1f45aec8608e7cd8bc3))

### Feature

* feat: deprecated CLI command `cyclonedx-bom` prints deprecation warning on STDERR before execution (#489)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`2009236`](https://github.com/CycloneDX/cyclonedx-python/commit/2009236c537af212aab1d5907e02f2b003f3062c))

### Unknown

* 3.11.0

Automatically generated by python-semantic-release ([`fe5ea31`](https://github.com/CycloneDX/cyclonedx-python/commit/fe5ea31ef5e6c33702b7cb63064b7a21e177fd49))


## v3.10.1 (2022-12-15)

### Documentation

* docs: improve CONTRIBUTION instructions - sign-off step (#470)



Signed-off-by: Roland Weber &lt;rolweber@de.ibm.com&gt; ([`578c0a8`](https://github.com/CycloneDX/cyclonedx-python/commit/578c0a88e63c804b1462e3d3b617f56b53b6012e))

### Fix

* fix: PURL for PyPI packages from &#39;conda list&#39; have the correct format now (#471)



Signed-off-by: Roland Weber &lt;rolweber@de.ibm.com&gt; ([`1573064`](https://github.com/CycloneDX/cyclonedx-python/commit/157306483a21583d752714a77ad7d0c7395291e5))

### Unknown

* 3.10.1

Automatically generated by python-semantic-release ([`7b44aea`](https://github.com/CycloneDX/cyclonedx-python/commit/7b44aeab491be5f91cb3fc895b9429c4dfe01ecc))


## v3.10.0 (2022-12-13)

### Feature

* feat: add support for poetry lock format v2.0 (#469)



Signed-off-by: tewfik-ghariani &lt;tewfik.ghariani@1und1.de&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Co-authored-by: tewfik-ghariani &lt;tewfik.ghariani@1und1.de&gt; ([`0b1e07f`](https://github.com/CycloneDX/cyclonedx-python/commit/0b1e07f91aada201088605a84ea394182ce0f10e))

### Unknown

* 3.10.0

Automatically generated by python-semantic-release ([`2501bed`](https://github.com/CycloneDX/cyclonedx-python/commit/2501bedfb72a48ba8418ba9c0b11710f9b1fb135))


## v3.9.0 (2022-12-13)

### Feature

* feat: parsers can outbut more debug messages (#466)



Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`9eedb4f`](https://github.com/CycloneDX/cyclonedx-python/commit/9eedb4ff27bb81f4ad323e9fa0f79230b0710032))

### Unknown

* 3.9.0

Automatically generated by python-semantic-release ([`895f597`](https://github.com/CycloneDX/cyclonedx-python/commit/895f5971b5e14031eb464b4038a3adce0a810f2d))


## v3.8.0 (2022-12-12)

### Feature

* feat: error- and debug-output is send to STDERR, instead of STDOUT (#465)


Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`f543b69`](https://github.com/CycloneDX/cyclonedx-python/commit/f543b69ee4463df3fb4d4b7c86475562f62e4744))

### Unknown

* 3.8.0

Automatically generated by python-semantic-release ([`24c4163`](https://github.com/CycloneDX/cyclonedx-python/commit/24c4163d4dd2d17fd7aa62e088c33bc7615625e9))


## v3.7.4 (2022-12-12)

### Chore

* chore: dependabot fix config

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`889a83e`](https://github.com/CycloneDX/cyclonedx-python/commit/889a83e4959391d010e536e3ed72f6ddf7a5cb1f))

* chore: dependabot interval weekly (#454)


Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`876ed30`](https://github.com/CycloneDX/cyclonedx-python/commit/876ed30b55300ad4abd4b078609d1b8d6e0e08a5))

### Fix

* fix: ignore broken licenses in env parser (#463)



Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3118acd`](https://github.com/CycloneDX/cyclonedx-python/commit/3118acdf180b6d8d35a637b3e94dc6ec7c5c5b3d))

### Unknown

* 3.7.4

Automatically generated by python-semantic-release ([`de188b8`](https://github.com/CycloneDX/cyclonedx-python/commit/de188b82fd05dcf3010095263c1a93bc1a5ca662))


## v3.7.3 (2022-12-11)

### Chore

* chore: Bump flake8-bugbear from 22.8.23 to 22.9.23 (#422)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.8.23 to 22.9.23.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.8.23...22.9.23)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`b05c55a`](https://github.com/CycloneDX/cyclonedx-python/commit/b05c55a7f191521a4d0b4bda29bdef3d250d8b4a))

### Ci

* ci: test dockerimage with more unique version identifier (#453)


Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`5a7fb9a`](https://github.com/CycloneDX/cyclonedx-python/commit/5a7fb9a374b336ee72852d8f4ccd9bcd0dfe0a36))

* ci: migrate `set-output` to `&gt;&gt; $GITHUB_OUTPUT` (#452)


Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`bf133a3`](https://github.com/CycloneDX/cyclonedx-python/commit/bf133a3c7a436a25bd6930eae7be435747c8b521))

* ci: fix py36 (#451)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b35e2bf`](https://github.com/CycloneDX/cyclonedx-python/commit/b35e2bfaf5703dc23fd9790114f014825a56404e))

### Fix

* fix: adjust dependency `pip-requirements-parser` to a working version (#450)



Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`6101986`](https://github.com/CycloneDX/cyclonedx-python/commit/610198659be408b5ef17d649aa381944d992a7dd))

### Unknown

* 3.7.3

Automatically generated by python-semantic-release ([`d425005`](https://github.com/CycloneDX/cyclonedx-python/commit/d4250057b3d2ed3e7b99bdd983d2b02945e78fc3))


## v3.7.2 (2022-11-15)

### Fix

* fix: add a missing space in the help pages `pathto` -&gt; `path to` (#443)

* docs: fix typo `pathto` -&gt; `path to`
* fix(help): added the missing space `pathto` -&gt; `path to`

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;
Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`bc5fe57`](https://github.com/CycloneDX/cyclonedx-python/commit/bc5fe5760565e608387ad7638126869550d65213))

### Unknown

* 3.7.2

Automatically generated by python-semantic-release ([`7aff239`](https://github.com/CycloneDX/cyclonedx-python/commit/7aff239caa22c6a4d7bc1dcbe6a1f1439dc0bf8f))


## v3.7.1 (2022-11-10)

### Chore

* chore(dep): bump and devide `coverage` (#438)

* chore(deps): bump `coverage`
* chore(deps): bump `coverage` locked

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`db051d1`](https://github.com/CycloneDX/cyclonedx-python/commit/db051d12660c5b6cc8209234a48f51b9e0657cec))

### Ci

* ci: enable py311 &amp; bump `poetry` (#437)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b7d5a4e`](https://github.com/CycloneDX/cyclonedx-python/commit/b7d5a4eb09e2348df34942d2afdf2a149efd9378))

* ci: fix python-version for static-code-analysis (#439)


Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`86daf68`](https://github.com/CycloneDX/cyclonedx-python/commit/86daf688a12c385406422dae3a582a48d0ca5e82))

### Fix

* fix(EnvironmentParser): reduced crashes if no Classifiers are found (#441)

fixes #440

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`67f56e7`](https://github.com/CycloneDX/cyclonedx-python/commit/67f56e7bfa4fb9d50654ebd07ece1ad14377a355))

### Unknown

* 3.7.1

Automatically generated by python-semantic-release ([`b2a97e0`](https://github.com/CycloneDX/cyclonedx-python/commit/b2a97e0328c4fb720717ff2233c357b76b1b73e7))


## v3.7.0 (2022-11-10)

### Feature

* feat: pass purl-bom-ref to EnvironmentParser (#432)



Signed-off-by: a1lu &lt;github.foreshoe@slmail.me&gt; ([`7cfefeb`](https://github.com/CycloneDX/cyclonedx-python/commit/7cfefeb389b3c63b69ad93aeca1a709231da2901))

### Unknown

* 3.7.0

Automatically generated by python-semantic-release ([`8c9a65a`](https://github.com/CycloneDX/cyclonedx-python/commit/8c9a65a17daf6feaa30dbe934235ce1ac67a43eb))


## v3.6.4 (2022-11-10)

### Fix

* fix(EnvironmentParser): remove code break when classifier parsing in py&gt;=3.8 (#431)



Signed-off-by: a1lu &lt;github.foreshoe@slmail.me&gt; ([`4ab075e`](https://github.com/CycloneDX/cyclonedx-python/commit/4ab075ee814571a8dc8c1e7b962686b232619330))

### Unknown

* 3.6.4

Automatically generated by python-semantic-release ([`f718356`](https://github.com/CycloneDX/cyclonedx-python/commit/f7183563ca812aa92fd267e588447fe45de1810b))


## v3.6.3 (2022-09-19)

### Fix

* fix: CI release pipeline

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`99ccdc6`](https://github.com/CycloneDX/cyclonedx-python/commit/99ccdc671f5a7a941f31199813bce71405bbfdd8))

### Unknown

* 3.6.3

Automatically generated by python-semantic-release ([`ddea61e`](https://github.com/CycloneDX/cyclonedx-python/commit/ddea61e60ccef20a1b3237af4f30340d1d76bc26))


## v3.6.2 (2022-09-19)

### Chore

* chore: Bump packageurl-python from 0.9.9 to 0.10.3 (#416)

Bumps [packageurl-python](https://github.com/package-url/packageurl-python) from 0.9.9 to 0.10.3.
- [Release notes](https://github.com/package-url/packageurl-python/releases)
- [Changelog](https://github.com/package-url/packageurl-python/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/package-url/packageurl-python/compare/v0.9.9...v0.10.3)

---
updated-dependencies:
- dependency-name: packageurl-python
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`2d6dade`](https://github.com/CycloneDX/cyclonedx-python/commit/2d6dadef49c6c2fb6bafb2ef10702125f2af11cb))

### Fix

* fix: CI release pipeline

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`6515071`](https://github.com/CycloneDX/cyclonedx-python/commit/6515071fc95d2b460577d0fbceb7d6c34a18c508))

### Unknown

* 3.6.2

Automatically generated by python-semantic-release ([`0a8f8ff`](https://github.com/CycloneDX/cyclonedx-python/commit/0a8f8ffd9978e59e1c158c981c410d2788ecafb4))


## v3.6.1 (2022-09-19)

### Fix

* fix: properly declare licenses from environment (#417)

use named licenses instead of license expressions.

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`25f9e29`](https://github.com/CycloneDX/cyclonedx-python/commit/25f9e29a162f20918b6f1bbe887cc7b18c623c16))

### Unknown

* 3.6.1

Automatically generated by python-semantic-release ([`89c262a`](https://github.com/CycloneDX/cyclonedx-python/commit/89c262a86f73d97f86b8d7605ba9ad4d4f52b00c))


## v3.6.0 (2022-09-16)

### Chore

* chore: package manifest fix link to homepage and documentation (#401)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`aa5ba35`](https://github.com/CycloneDX/cyclonedx-python/commit/aa5ba35a3677d8ebf5ac4643b2d403003267ef8b))

* chore: fix poetry in tox (#411)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b5ceec5`](https://github.com/CycloneDX/cyclonedx-python/commit/b5ceec5f3fb58959a20c26db85316b39e522b8a2))

* chore: Bump flake8-bugbear from 22.8.22 to 22.8.23 (#404)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.8.22 to 22.8.23.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.8.22...22.8.23)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`37f18f8`](https://github.com/CycloneDX/cyclonedx-python/commit/37f18f88337bbfa89f5a40fa203d22aad6b852ef))

* chore: Bump flake8-bugbear from 22.7.1 to 22.8.22 (#403)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.7.1 to 22.8.22.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.7.1...22.8.22)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`1b6e7a0`](https://github.com/CycloneDX/cyclonedx-python/commit/1b6e7a062f8598187122599305eebbad5c76915a))

* chore: Bump flake8-isort from 4.1.1 to 4.2.0 (#400)

Bumps [flake8-isort](https://github.com/gforcada/flake8-isort) from 4.1.1 to 4.2.0.
- [Release notes](https://github.com/gforcada/flake8-isort/releases)
- [Changelog](https://github.com/gforcada/flake8-isort/blob/master/CHANGES.rst)
- [Commits](https://github.com/gforcada/flake8-isort/compare/4.1.1...4.2.0)

---
updated-dependencies:
- dependency-name: flake8-isort
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`b4275e7`](https://github.com/CycloneDX/cyclonedx-python/commit/b4275e7943d4428805c8533da386313c1229a83a))

* chore: Bump types-toml from 0.10.7 to 0.10.8 (#387)

Bumps [types-toml](https://github.com/python/typeshed) from 0.10.7 to 0.10.8.
- [Release notes](https://github.com/python/typeshed/releases)
- [Commits](https://github.com/python/typeshed/commits)

---
updated-dependencies:
- dependency-name: types-toml
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`4a68f5f`](https://github.com/CycloneDX/cyclonedx-python/commit/4a68f5fd47c657735f57dceb66c9625d0839e2b3))

* chore: Bump mypy from 0.961 to 0.971 (#390)

Bumps [mypy](https://github.com/python/mypy) from 0.961 to 0.971.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.961...v0.971)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`f2a7ec4`](https://github.com/CycloneDX/cyclonedx-python/commit/f2a7ec4b2c4919e32d73957e22fb320fb9ca843c))

* chore: Bump tox from 3.25.0 to 3.25.1 (#384)

Bumps [tox](https://github.com/tox-dev/tox) from 3.25.0 to 3.25.1.
- [Release notes](https://github.com/tox-dev/tox/releases)
- [Changelog](https://github.com/tox-dev/tox/blob/master/docs/changelog.rst)
- [Commits](https://github.com/tox-dev/tox/compare/3.25.0...3.25.1)

---
updated-dependencies:
- dependency-name: tox
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`cfd4a73`](https://github.com/CycloneDX/cyclonedx-python/commit/cfd4a736e2e8df83d6d998cadb68eeb822d6a8b1))

* chore: Bump flake8-bugbear from 22.6.22 to 22.7.1 (#385)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.6.22 to 22.7.1.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.6.22...22.7.1)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`3ac5df9`](https://github.com/CycloneDX/cyclonedx-python/commit/3ac5df95f45675c1780b6c8cb7a9e2ecf422da81))

### Documentation

* docs: describe `cyclonedx-py` rather than `cyclonedx-bom`

fixes #414

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`c04196e`](https://github.com/CycloneDX/cyclonedx-python/commit/c04196e4404efc0513676e5baefeaf03e6b3b8e3))

* docs: Minor updates to poetry usage details &amp; contributing.md (#407)

* docs: fix minor typo in poetry usage docs
* docs: update commit flag in contribution guidelines

Signed-off-by: Emily Schultz &lt;emilyschultz16@gmail.com&gt; ([`0abe230`](https://github.com/CycloneDX/cyclonedx-python/commit/0abe23049b5423f55b3e0951a00047f4e3f93056))

### Feature

* feat: enable dependency `cyclonedx-python-lib@^3` (#418)


Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`05cd51e`](https://github.com/CycloneDX/cyclonedx-python/commit/05cd51e1da261d29fb5c3e1722544a8f00a0cfcd))

### Unknown

* 3.6.0

Automatically generated by python-semantic-release ([`049a5b3`](https://github.com/CycloneDX/cyclonedx-python/commit/049a5b353318e6f98f514051b442e99c9a90740a))

* Merge pull request #415 from CycloneDX/docs_cyclonedx-py

docs: describe command line usages as `cyclonedx-py` rather than `cyclonedx-bom` #414 ([`348f689`](https://github.com/CycloneDX/cyclonedx-python/commit/348f68900e97a1eac30b712298f1e75d88d55e5f))


## v3.5.0 (2022-06-27)

### Chore

* chore: Bump flake8-bugbear from 22.4.25 to 22.6.22 (#376)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.4.25 to 22.6.22.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.4.25...22.6.22)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`7139bb0`](https://github.com/CycloneDX/cyclonedx-python/commit/7139bb093e9c7b3585abaf193a2dee5a63c1ec1b))

### Feature

* feat: optionally force `bom_ref` to be `purl` rather that the default random UUID format - thanks @RodneyRichardson

Merge pull request #361 from RodneyRichardson/use-explicit-bom-ref ([`9659d08`](https://github.com/CycloneDX/cyclonedx-python/commit/9659d08f524fd1ea2eb34234f2449105feb93f62))

### Unknown

* 3.5.0

Automatically generated by python-semantic-release ([`d5465ec`](https://github.com/CycloneDX/cyclonedx-python/commit/d5465ecd67dfc16ebfa554c4cdaefcebc2f17665))

* Update README.md with purl-bom-ref parameter.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`b9b3a01`](https://github.com/CycloneDX/cyclonedx-python/commit/b9b3a0151d74b0e1dec2a37aaa011176deba7a6f))

* Add CLI option to use purl as bom-ref.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`d609ec3`](https://github.com/CycloneDX/cyclonedx-python/commit/d609ec3dc00ae01aa9aec96e6717cb7dcf2b3550))

* Remove unnecessary str() cast.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`b1f9895`](https://github.com/CycloneDX/cyclonedx-python/commit/b1f9895d5278f794b119b655321670edd788a77c))

* Merge branch &#39;CycloneDX:master&#39; into use-explicit-bom-ref ([`23d10bf`](https://github.com/CycloneDX/cyclonedx-python/commit/23d10bfd9800240550a4e1d089447d1275c9ca71))

* Merge branch &#39;master&#39; into use-explicit-bom-ref ([`f89f706`](https://github.com/CycloneDX/cyclonedx-python/commit/f89f7067e4fdbc6c09463d8631f509bd2aa1c4c5))

*  chore: Bump cyclonedx-python-lib from 2.4.0 to 2.5.2 (#373)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a9bbe5e`](https://github.com/CycloneDX/cyclonedx-python/commit/a9bbe5e49a6d3cdbd8b4a63ef4d5c8d9189a722e))


## v3.4.0 (2022-06-16)

### Feature

* feat: Update purl to match specification when ingesting packages from Conda - thanks to @RodneyRichardson ([`072c8f1`](https://github.com/CycloneDX/cyclonedx-python/commit/072c8f11bdef44abb0c6f7f7e99e2b833ab1c875))

### Unknown

* 3.4.0

Automatically generated by python-semantic-release ([`cf7c625`](https://github.com/CycloneDX/cyclonedx-python/commit/cf7c6255d51d54633fd86d12d44ceac54ef8a001))

* Merge branch &#39;master&#39; into fix-conda-purl ([`2999022`](https://github.com/CycloneDX/cyclonedx-python/commit/29990223c475f1445d6c04654569517417e5d65e))


## v3.3.0 (2022-06-16)

### Chore

* chore: Bump actions/setup-python from 3 to 4 (#369)

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 3 to 4.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/v3...v4)

---
updated-dependencies:
- dependency-name: actions/setup-python
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`eecf04a`](https://github.com/CycloneDX/cyclonedx-python/commit/eecf04ac95f8beb0a32488a0f6b57d082f632214))

* chore: Bump mypy from 0.960 to 0.961 (#365)

Bumps [mypy](https://github.com/python/mypy) from 0.960 to 0.961.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.960...v0.961)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`3bab869`](https://github.com/CycloneDX/cyclonedx-python/commit/3bab86909701f7e6a3af8815969625aeed2dfdc4))

* chore: Bump mypy from 0.942 to 0.960 (#356)

* chore: Bump mypy from 0.942 to 0.960

Bumps [mypy](https://github.com/python/mypy) from 0.942 to 0.960.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.942...v0.960)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

* chore: try type fixes

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt;
Co-authored-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b62fc5e`](https://github.com/CycloneDX/cyclonedx-python/commit/b62fc5e2e8bfe2f85765b0e566f4d119dee20b8b))

### Feature

* feat: Add Conda MD5 hash to Component.hashes, if available - thanks @RodneyRichardson ([`772c517`](https://github.com/CycloneDX/cyclonedx-python/commit/772c517521da0fd8ddbd1ed8abdf22243f418217))

### Test

* test: extend `TestRequirementsParser` to check `hashes` (#368)

* Extend TestRequirementsParser.test_example_with_hashes() to check hashes

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt;

* Add additional test for hash.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`e2be444`](https://github.com/CycloneDX/cyclonedx-python/commit/e2be444b8db7dd12031f3e9b481dfdae23f3e59e))

### Unknown

* 3.3.0

Automatically generated by python-semantic-release ([`b028c2b`](https://github.com/CycloneDX/cyclonedx-python/commit/b028c2b96fb2caea2d7f084b6ef88cba1bcade2b))

* Merge branch &#39;master&#39; into fix-conda-purl ([`cf4a5e4`](https://github.com/CycloneDX/cyclonedx-python/commit/cf4a5e4f66c0c934c10ba06aecb42641eb201470))

* Merge branch &#39;master&#39; into add-conda-hash ([`95c6893`](https://github.com/CycloneDX/cyclonedx-python/commit/95c68932e3aa24cf7b83e2e1139928a95b71f8d6))

* Merge branch &#39;master&#39; into use-explicit-bom-ref

# Conflicts:
#	tests/test_parser_requirements.py

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`d5d0160`](https://github.com/CycloneDX/cyclonedx-python/commit/d5d0160e3e3fc35efb0037586aadd84160304774))

* Ignore missing typing for packageurl

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`5ac29c5`](https://github.com/CycloneDX/cyclonedx-python/commit/5ac29c5cb9fbd47e8d060b421cef66d4c8dcc9a4))

* Explicitly cast package_format to str.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`31d5daf`](https://github.com/CycloneDX/cyclonedx-python/commit/31d5dafaf999da8939618138cb86f474750446eb))

* Cast md5_hash to str

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`51afacf`](https://github.com/CycloneDX/cyclonedx-python/commit/51afacf997343c2ebcab998b1f02c78051dea040))

* Fix sonatype-lift warning.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`5e60fac`](https://github.com/CycloneDX/cyclonedx-python/commit/5e60face658c74a4a6b549d091c2a440b25e9869))

* Add Conda MD5 hash to Component.hashes, if available

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`54c33b5`](https://github.com/CycloneDX/cyclonedx-python/commit/54c33b56fd717ca9481294191a24cca5658c7c2b))

* Update Conda purl to match specification

Add conda_package_to_purl() utility function
Add package_format field to CondaPackage
purl specification can be found here: https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst#conda

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`e392cbc`](https://github.com/CycloneDX/cyclonedx-python/commit/e392cbced269608b67d5bee7482843fc45e30586))

* Merge branch &#39;CycloneDX:master&#39; into use-explicit-bom-ref ([`c99d993`](https://github.com/CycloneDX/cyclonedx-python/commit/c99d9931f4432266f430505598deec61772010c8))


## v3.2.2 (2022-06-02)

### Chore

* chore: Bump cyclonedx-python-lib from 2.1.0 to 2.4.0 (#353)

Bumps [cyclonedx-python-lib](https://github.com/CycloneDX/cyclonedx-python-lib) from 2.1.0 to 2.4.0.
- [Release notes](https://github.com/CycloneDX/cyclonedx-python-lib/releases)
- [Changelog](https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/CHANGELOG.md)
- [Commits](https://github.com/CycloneDX/cyclonedx-python-lib/compare/v2.1.0...v2.4.0)

---
updated-dependencies:
- dependency-name: cyclonedx-python-lib
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`350297e`](https://github.com/CycloneDX/cyclonedx-python/commit/350297ee11cfaa312f4d4d08b983ac7c3d0ca719))

* chore: Bump flake8-bugbear from 22.3.23 to 22.4.25 (#351)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.3.23 to 22.4.25.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.3.23...22.4.25)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`ecfb175`](https://github.com/CycloneDX/cyclonedx-python/commit/ecfb17560f1be39e1d28aa64f009344871db4162))

* chore: Bump tox from 3.24.5 to 3.25.0 (#345)

Bumps [tox](https://github.com/tox-dev/tox) from 3.24.5 to 3.25.0.
- [Release notes](https://github.com/tox-dev/tox/releases)
- [Changelog](https://github.com/tox-dev/tox/blob/master/docs/changelog.rst)
- [Commits](https://github.com/tox-dev/tox/compare/3.24.5...3.25.0)

---
updated-dependencies:
- dependency-name: tox
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`194d287`](https://github.com/CycloneDX/cyclonedx-python/commit/194d2878fe088f8f1a680cc4eb95504c046d34a2))

* chore: Bump actions/download-artifact from 2 to 3 (#343)

Bumps [actions/download-artifact](https://github.com/actions/download-artifact) from 2 to 3.
- [Release notes](https://github.com/actions/download-artifact/releases)
- [Commits](https://github.com/actions/download-artifact/compare/v2...v3)

---
updated-dependencies:
- dependency-name: actions/download-artifact
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`259351e`](https://github.com/CycloneDX/cyclonedx-python/commit/259351ea468c7d7642be4640783e76826a56d39a))

* chore: Bump actions/upload-artifact from 2 to 3 (#342)

Bumps [actions/upload-artifact](https://github.com/actions/upload-artifact) from 2 to 3.
- [Release notes](https://github.com/actions/upload-artifact/releases)
- [Commits](https://github.com/actions/upload-artifact/compare/v2...v3)

---
updated-dependencies:
- dependency-name: actions/upload-artifact
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`4b74fa0`](https://github.com/CycloneDX/cyclonedx-python/commit/4b74fa064b40051bbe0e2aad298caecff6ef7940))

### Ci

* ci: pin GH-action `semantic-release` to v7.28.1 (#359)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`ec417c7`](https://github.com/CycloneDX/cyclonedx-python/commit/ec417c7418b3eef456c90bccb1bc8c29f038beca))

* ci: introduce `timeout-minutes` and drop `dependabot` branches for CI #344

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`3591849`](https://github.com/CycloneDX/cyclonedx-python/commit/359184951f18a49c7c6dd47f7e0945a215507360))

* ci: introduce `timeout-minutes` and drop `dependabot` branches for CI

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`72c4967`](https://github.com/CycloneDX/cyclonedx-python/commit/72c4967ccad4ceabb2367177c90c0a80388193b7))

### Fix

* fix: add actively used (transitive) dependencies (#363)

* ci: add test with lowest dependencies
* fix: have some typings corrected
* fix: add actively used (transitive) dependencies

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`1f45ad9`](https://github.com/CycloneDX/cyclonedx-python/commit/1f45ad9162be511f07e9310414793218c554a097))

### Unknown

* 3.2.2

Automatically generated by python-semantic-release ([`f3f40c8`](https://github.com/CycloneDX/cyclonedx-python/commit/f3f40c8cc648a5d116a892bdd6ff9bf067133542))

* Use purl.to_string() as default bom_ref for Components.

Signed-off-by: Rodney Richardson &lt;rodney.richardson@cambridgeconsultants.com&gt; ([`0c8dd60`](https://github.com/CycloneDX/cyclonedx-python/commit/0c8dd608adeb9861e0d2312cdf7ff14a059c8edb))

* Merge pull request #348 from sleightsec/include-pipenv-hashes-without-index-attribute

fix: remove check for `index==pypi` which causes hashes to be excluded from the resultant BOM when using PipEnv Parser ([`ae537fb`](https://github.com/CycloneDX/cyclonedx-python/commit/ae537fb4106f14dfd4bf5eb78a17f67ce95cf204))

* correct test for dependencies with hashes and no index attribute in pipenv

Signed-off-by: sleightsec &lt;69399725+sleightsec@users.noreply.github.com&gt; ([`b9ab033`](https://github.com/CycloneDX/cyclonedx-python/commit/b9ab033c7251cc5257fd0069eb0d1c76c85a27ef))

* #347 - remove index=pypi attribute requirement for pipenv hash inclusion

Signed-off-by: sleightsec &lt;69399725+sleightsec@users.noreply.github.com&gt; ([`65bf318`](https://github.com/CycloneDX/cyclonedx-python/commit/65bf3181c61382186cafb67c25d2583fa5a53637))


## v3.2.1 (2022-04-05)

### Unknown

* 3.2.1

Automatically generated by python-semantic-release ([`092bdf2`](https://github.com/CycloneDX/cyclonedx-python/commit/092bdf260349a2d5dc20faf8007fbda1ff2bba18))

* Merge pull request #338 from CycloneDX/bugfix/json-format-default-file

fix: cli default file name for json format ([`929e26d`](https://github.com/CycloneDX/cyclonedx-python/commit/929e26d504f158f775f00b1f44669e02d5e4f536))


## v3.2.0 (2022-04-05)

### Chore

* chore: Bump cyclonedx-python-lib from 2.0.0 to 2.1.0 (#340)

Bumps [cyclonedx-python-lib](https://github.com/CycloneDX/cyclonedx-python-lib) from 2.0.0 to 2.1.0.
- [Release notes](https://github.com/CycloneDX/cyclonedx-python-lib/releases)
- [Changelog](https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/CHANGELOG.md)
- [Commits](https://github.com/CycloneDX/cyclonedx-python-lib/compare/v2.0.0...v2.1.0)

---
updated-dependencies:
- dependency-name: cyclonedx-python-lib
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`171aafe`](https://github.com/CycloneDX/cyclonedx-python/commit/171aafe8daf2ca3fc0ec15b7aa2d0cacf3c208e4))

* chore: Bump mypy from 0.941 to 0.942 (#339)

Bumps [mypy](https://github.com/python/mypy) from 0.941 to 0.942.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.941...v0.942)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`7cb551c`](https://github.com/CycloneDX/cyclonedx-python/commit/7cb551c182d05d3cc54bf2c5cca5f408c96fa4cd))

* chore: Bump flake8-bugbear from 22.3.20 to 22.3.23 (#336)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.3.20 to 22.3.23.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.3.20...22.3.23)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`11fcb60`](https://github.com/CycloneDX/cyclonedx-python/commit/11fcb60d8be0e95ad44e2b3d6d7431c9a1e018e1))

* chore: dependabot prefixes with `chore` and scope (#324)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`1985b56`](https://github.com/CycloneDX/cyclonedx-python/commit/1985b56ba235e48e79071667bc1425c0a3552974))

### Fix

* fix: cli default file for json format

fixes #337

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`8747620`](https://github.com/CycloneDX/cyclonedx-python/commit/8747620dac7ed3eeff69369c05dfb6386a56e549))

### Test

* test: fix malformed or wrong test setups (#333)

* test: corrected malformed/broken tests

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* test: fix tests and fixtures

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt;

* test: corrected malformed/broken tests

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* fix: fix style and remove unnecessary package

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt;
Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

Co-authored-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`0ff6493`](https://github.com/CycloneDX/cyclonedx-python/commit/0ff6493dd59d2e8efafd35d4460847525e590937))

### Unknown

* 3.2.0

Automatically generated by python-semantic-release ([`eb054b0`](https://github.com/CycloneDX/cyclonedx-python/commit/eb054b05a6003b30e1a7ed85f5f6dc399c41f85e))

* Merge pull request #326 from CycloneDX/callable-module

feat: make package/module callable ([`193f1a4`](https://github.com/CycloneDX/cyclonedx-python/commit/193f1a491c042beac67c1e519bd0862e899faea1))

* shield icons in README ([`b647219`](https://github.com/CycloneDX/cyclonedx-python/commit/b64721995c731c00b22011b7ba62ae21207d38fc))


## v3.1.1 (2022-03-21)

### Chore

* chore: Bump flake8-bugbear from 22.1.11 to 22.3.20 (#335)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 22.1.11 to 22.3.20.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/22.1.11...22.3.20)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`5e344e2`](https://github.com/CycloneDX/cyclonedx-python/commit/5e344e223a19048c896b394bf1e6fe1a3a8d4855))

* chore: Bump mypy from 0.940 to 0.941 (#330)

Bumps [mypy](https://github.com/python/mypy) from 0.940 to 0.941.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.940...v0.941)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`c02d770`](https://github.com/CycloneDX/cyclonedx-python/commit/c02d770cf18a57e118347a0a57db29ae65919c35))

* chore: Bump mypy from 0.931 to 0.940 (#329)

Bumps [mypy](https://github.com/python/mypy) from 0.931 to 0.940.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.931...v0.940)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`133ef9f`](https://github.com/CycloneDX/cyclonedx-python/commit/133ef9f432253923b7533852cbf5ba637363002e))

### Documentation

* docs: describe methods to call the tool

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`2bac83a`](https://github.com/CycloneDX/cyclonedx-python/commit/2bac83a6c6f7354d8b7218c32b4b2e5d96b2fd0c))

* docs: add link to https://cyclonedx.org/ to README

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`fc4b8e4`](https://github.com/CycloneDX/cyclonedx-python/commit/fc4b8e44bec39b175bb8994e0a59bc5076d1b2a6))

* docs: add hint for RTFD to README

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`cf4f534`](https://github.com/CycloneDX/cyclonedx-python/commit/cf4f534401dc90dbe093ce1a094efb02e5fb7c90))

* docs: add RTFD shield to README

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`7fef6ee`](https://github.com/CycloneDX/cyclonedx-python/commit/7fef6eec5d553c7687e7b2d2af1ba4e330f16490))

* docs: fixed link to RTFD

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3a8669a`](https://github.com/CycloneDX/cyclonedx-python/commit/3a8669ad7ba4230d06d1e0965342a5a836a52d1f))

### Feature

* feat: make module callable

fixes #321

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`5b3d8d7`](https://github.com/CycloneDX/cyclonedx-python/commit/5b3d8d7641b0f2825e5419b5ad8c8a75bf66403b))

### Fix

* fix(conda-parser): version recognition for strings (#332)

conda packacge string parser no longer raises unexpected errors,
if the build-number is non-numeric.
fixes #331

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`65246dd`](https://github.com/CycloneDX/cyclonedx-python/commit/65246ddfa9a55ce53fbf87f33b1f269c519f9b3a))

### Unknown

* 3.1.1

Automatically generated by python-semantic-release ([`f5d7943`](https://github.com/CycloneDX/cyclonedx-python/commit/f5d7943f28b19af836139699f6fd0e95806b317d))

* Merge pull request #328 from CycloneDX/docs-hint-to-rtd

docs: add and fix hint to rtfd ([`3b3477b`](https://github.com/CycloneDX/cyclonedx-python/commit/3b3477bc8c79f46208ad46568082ceca036cac2f))


## v3.1.0 (2022-03-10)

### Chore

* chore: added documentation to CONTRIBUTING guidelines

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`8d7d6b6`](https://github.com/CycloneDX/cyclonedx-python/commit/8d7d6b638d22309124c8dc80aa494590cce9422d))

* chore: Bump actions/setup-python from 2 to 3 (#322)

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 2 to 3.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/v2...v3)

---
updated-dependencies:
- dependency-name: actions/setup-python
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`69de237`](https://github.com/CycloneDX/cyclonedx-python/commit/69de237fb6bd327f7e2a6f1047122dfafb65e388))

* chore: Bump actions/checkout from 2.4.0 to 3 (#323)

Bumps [actions/checkout](https://github.com/actions/checkout) from 2.4.0 to 3.
- [Release notes](https://github.com/actions/checkout/releases)
- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
- [Commits](https://github.com/actions/checkout/compare/v2.4.0...v3)

---
updated-dependencies:
- dependency-name: actions/checkout
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`cae737f`](https://github.com/CycloneDX/cyclonedx-python/commit/cae737f2b6fcbb9c44f7d6602260bc460da23858))

* chore: make isort and flake8-isort available

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`c6b561e`](https://github.com/CycloneDX/cyclonedx-python/commit/c6b561eabfbfb81c29ab0a44056d08e55cd23a91))

* chore: manually fixed CHANGELOG after accidental 2.1.0

2.1.0 should have been 3.0.0 ([`33c4437`](https://github.com/CycloneDX/cyclonedx-python/commit/33c4437aec7c29b331bbbf8e9abb63b86c6f6964))

### Documentation

* docs: update RequirementsFileParser docs to include nested file support

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`9e9021d`](https://github.com/CycloneDX/cyclonedx-python/commit/9e9021decb19d8262e87fe6955577c1bd1309d95))

### Feature

* feat: Add pip-requirements-parser and update virtualenv to latest version

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`73b2182`](https://github.com/CycloneDX/cyclonedx-python/commit/73b2182550d9635a0a5ab8e4f2226f37cf6b1b35))

### Fix

* fix: sort imports

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`fdec44b`](https://github.com/CycloneDX/cyclonedx-python/commit/fdec44bc111d7eb1add080a219dbc77744678f8a))

* fix: Try to fix the temp file issue on Windows machines

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`684d4f0`](https://github.com/CycloneDX/cyclonedx-python/commit/684d4f03ad6f8c0764dfaf8f3a38a09b91b69e5d))

### Refactor

* refactor: Apply suggestions by @jkowalleck

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`90b336f`](https://github.com/CycloneDX/cyclonedx-python/commit/90b336ff4a0b49176162e6d2ea4c25faa21e3d99))

* refactor: ignore mypy type errors and add proper annotation to _TemporaryFileWrapper

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`82cb655`](https://github.com/CycloneDX/cyclonedx-python/commit/82cb6556927aacf911ee69fef86006c5c6ca7e76))

* refactor: remove unnecessary import (flake8 error)

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`ef8148f`](https://github.com/CycloneDX/cyclonedx-python/commit/ef8148f05c31a2d254cb72048f20f98dce450aef))

* refactor: Replace requirements file parser

feat: Add support for hashes, local packages and private repositories
Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`addc21a`](https://github.com/CycloneDX/cyclonedx-python/commit/addc21ae832f642298f665d426c576822038fb2f))

### Style

* style: sort imports

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`75d325d`](https://github.com/CycloneDX/cyclonedx-python/commit/75d325d2872b01e3cfb31883fb4044c5b7991609))

* style: sorted all imports

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`804420a`](https://github.com/CycloneDX/cyclonedx-python/commit/804420afc9bb02ac01c04c18fa0828024688bd42))

### Test

* test: add remote URL as requirements line

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`4be30e2`](https://github.com/CycloneDX/cyclonedx-python/commit/4be30e29aa7da993dedc66560d5df7360932fd7e))

* test: add test for nested requirements file parsing

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`d0856e9`](https://github.com/CycloneDX/cyclonedx-python/commit/d0856e90743926648977f91981cfda500502fc51))

* test: Add test for Git URLs

Signed-off-by: Mostafa Moradian &lt;mostafamoradian0@gmail.com&gt; ([`25333c4`](https://github.com/CycloneDX/cyclonedx-python/commit/25333c4e4bb041373fea06489ea672e5e2db176f))

### Unknown

* 3.1.0

Automatically generated by python-semantic-release ([`92b21f7`](https://github.com/CycloneDX/cyclonedx-python/commit/92b21f7310c85c155cff156361acc7a816ce65a4))

* Merge pull request #327 from mostafa/feat/parse-requirements-txt-with-locally-referenced-packages

feat: Change requirements parser ([`f973c91`](https://github.com/CycloneDX/cyclonedx-python/commit/f973c9159eaed852c5acb7804f9cbe61f480f9c8))

* Merge pull request #320 from CycloneDX/sort-imports

style: sort imports ([`a527e0d`](https://github.com/CycloneDX/cyclonedx-python/commit/a527e0df9d83ca2c756cac19079c00a59ad21d55))


## v3.0.0 (2022-02-21)

### Breaking

* feat: bump to latest `cyclonedx-python-lib`

BREAKING CHANGE: Default Schema Version has been replaced by notion of LATEST supported Schema Version

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`5902fbf`](https://github.com/CycloneDX/cyclonedx-python/commit/5902fbf9dc5becdf7d92180242488e56b998d9de))

### Feature

* feat: added marker and classifiers to denote this as typed (#313)

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`f317353`](https://github.com/CycloneDX/cyclonedx-python/commit/f317353bd7a24dbf4fb31642d766d94da609eb42))

* feat: update to latest RC of `cyclonedx-python-lib`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`6c8b517`](https://github.com/CycloneDX/cyclonedx-python/commit/6c8b5173f07329b2086312d27af5d111f9b2c7ed))

* feat: update to latest RC of `cyclonedx-python-lib`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`bc8ee6b`](https://github.com/CycloneDX/cyclonedx-python/commit/bc8ee6bb115dd5214358430f64bd0581de5cb2e4))

### Unknown

* 3.0.0

Automatically generated by python-semantic-release ([`f7ca95c`](https://github.com/CycloneDX/cyclonedx-python/commit/f7ca95ceb0f7d7ab24db4fa59cb2474eb9d53329))

* Merge pull request #316 from CycloneDX/feat/update-lib-2.0.x

feat: bump to latest `cyclonedx-python-lib`

feat: Added marker and classifiers to denote this as typed (#313)

BREAKING CHANGE: bump to latest `cyclonedx-python-lib` ([`4700399`](https://github.com/CycloneDX/cyclonedx-python/commit/4700399a6ca9121324f361ce696a90f7345a8fc4))

* 2.1.0

Automatically generated by python-semantic-release ([`cc848f7`](https://github.com/CycloneDX/cyclonedx-python/commit/cc848f7773e15fed1298f2c4ca6e049412bf5ec5))

* Merge pull request #311 from CycloneDX/feat/update-lib-2.0.x

BREAKING CHANGE: update to latest RC of `cyclonedx-python-lib` ([`3cb14e0`](https://github.com/CycloneDX/cyclonedx-python/commit/3cb14e015ce531a1aad92d43686fe3a3d0f6f63f))

* bumped to latest RC of `cyclonedx-python-lib`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`e193521`](https://github.com/CycloneDX/cyclonedx-python/commit/e193521eeb56e41726ee6c8d9718d970313c5455))

* updated tests to be more Pythonic

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`891cf3e`](https://github.com/CycloneDX/cyclonedx-python/commit/891cf3ee00df9ca3f603990dac2d2f402bd9607f))

* bumped to latest RC of `cyclonedx-python-lib`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`54db3cd`](https://github.com/CycloneDX/cyclonedx-python/commit/54db3cd9fefa5fabd5820f0c901c2968dbc15c41))

* bump `cyclonedx-python-lib` rc

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`a4795ed`](https://github.com/CycloneDX/cyclonedx-python/commit/a4795ed7fbe095a57f26b3c76aeb5027fbdce3f8))

* BREAKING CHANGE: update so default schema version is 1.4

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`689e7e9`](https://github.com/CycloneDX/cyclonedx-python/commit/689e7e9a6d99a4589115777857e18488fe46b57c))


## v2.0.3 (2022-02-03)

### Fix

* fix: docker image releae checkout ref w/o `tags` (#309)

fixes #308

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`5d8b1e1`](https://github.com/CycloneDX/cyclonedx-python/commit/5d8b1e159c2ced59e810b9e9564e19a29fe263d0))

### Unknown

* 2.0.3

Automatically generated by python-semantic-release ([`8379712`](https://github.com/CycloneDX/cyclonedx-python/commit/837971222d1f3d5f62d3cdfcd84bb82b8fcc2e37))


## v2.0.2 (2022-02-03)

### Fix

* fix: properly support reading from stdin (#307)

* Adjust cli when reading from stdin.

Bind reading from stdin on specifying `-i -`. This is part of
[`argparse.FileType`](https://docs.python.org/3/library/argparse.html?highlight=pseudo-argument#argparse.FileType).

Local tests under the following conditions:

 * implicit reading `poetry.lock` using args `-p -o -`
 * explicit reading `poetry.lock` using args `-p -i poetry.lock -o -`
 * explicit reading `poetry.lock` file after renaming using
   `cat p.lock | python -m cyclonedx_py.client -p -i - -o -`

Signed-off-by: Theodor van Nahl &lt;theo@van-nahl.org&gt; ([`23f31a0`](https://github.com/CycloneDX/cyclonedx-python/commit/23f31a03a4fbf888f396b88a9413c054358b2a3a))

### Unknown

* 2.0.2

Automatically generated by python-semantic-release ([`916951a`](https://github.com/CycloneDX/cyclonedx-python/commit/916951a4ff13dd91140f93ecb079c5b5a31d5f27))

* Update CONTRIBUTING.md

link to pep8 ([`4f87341`](https://github.com/CycloneDX/cyclonedx-python/commit/4f87341ea847974a9cd89b753af3f9424267ff01))


## v2.0.1 (2022-01-24)

### Chore

* chore: add CI artifacts and improve build consistency (#290)

fixes #292
prep for #289

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`185b300`](https://github.com/CycloneDX/cyclonedx-python/commit/185b30071acc2fb310e4632a7a1b735b9cc9382e))

* chore: Bump flake8-bugbear from 21.11.29 to 22.1.11 (#301)

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 21.11.29 to 22.1.11.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/21.11.29...22.1.11)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`1b6e042`](https://github.com/CycloneDX/cyclonedx-python/commit/1b6e0422d6932dac0accbad78169b850602162ca))

* chore: Bump mypy from 0.930 to 0.931 (#297)

Bumps [mypy](https://github.com/python/mypy) from 0.930 to 0.931.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.930...v0.931)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`19b285c`](https://github.com/CycloneDX/cyclonedx-python/commit/19b285c9590cc4a66c07a32bcbbd54df8839dc7b))

* chore: corrected next version

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`ea8a963`](https://github.com/CycloneDX/cyclonedx-python/commit/ea8a9633f3a06c294a8c57a2169d1707af927e46))

### Fix

* fix: bump dependencies to get latest `cyclonedx-python-lib`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`87c3fe7`](https://github.com/CycloneDX/cyclonedx-python/commit/87c3fe7747cd8abd55ad5699bfc87ad9877c8132))

### Unknown

* 2.0.1

Automatically generated by python-semantic-release ([`a4a4c42`](https://github.com/CycloneDX/cyclonedx-python/commit/a4a4c427f1fe97231f6e93e13c477030a7a9eed9))


## v2.0.0 (2022-01-13)

### Build

* build(deps-dev): Bump coverage from 6.1.2 to 6.2

Bumps [coverage](https://github.com/nedbat/coveragepy) from 6.1.2 to 6.2.
- [Release notes](https://github.com/nedbat/coveragepy/releases)
- [Changelog](https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst)
- [Commits](https://github.com/nedbat/coveragepy/compare/6.1.2...6.2)

---
updated-dependencies:
- dependency-name: coverage
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`82f0dba`](https://github.com/CycloneDX/cyclonedx-python/commit/82f0dba359030b513e9fcf3f8e8c561afc794c1d))

* build(deps-dev): Bump flake8-bugbear from 21.9.2 to 21.11.29

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 21.9.2 to 21.11.29.
- [Release notes](https://github.com/PyCQA/flake8-bugbear/releases)
- [Commits](https://github.com/PyCQA/flake8-bugbear/compare/21.9.2...21.11.29)

---
updated-dependencies:
- dependency-name: flake8-bugbear
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`a3d0b87`](https://github.com/CycloneDX/cyclonedx-python/commit/a3d0b87152183682dfeed459c6e44af4bc69a8c8))

### Chore

* chore: add pre-release manual GH workflow

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`8343c0d`](https://github.com/CycloneDX/cyclonedx-python/commit/8343c0d20fe8ce2ffaf41016155dee7953f4eb57))

* chore: Bump cyclonedx-python-lib from 0.12.2 to 0.12.3 (#285)

Bumps [cyclonedx-python-lib](https://github.com/CycloneDX/cyclonedx-python-lib) from 0.12.2 to 0.12.3.
- [Release notes](https://github.com/CycloneDX/cyclonedx-python-lib/releases)
- [Changelog](https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/CHANGELOG.md)
- [Commits](https://github.com/CycloneDX/cyclonedx-python-lib/compare/v0.12.2...v0.12.3)

---
updated-dependencies:
- dependency-name: cyclonedx-python-lib
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`2ef2b3e`](https://github.com/CycloneDX/cyclonedx-python/commit/2ef2b3eb767ed45c329390abc2800927c6324948))

* chore: Bump mypy from 0.920 to 0.930 (#288)

Bumps [mypy](https://github.com/python/mypy) from 0.920 to 0.930.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.920...v0.930)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`a58ed74`](https://github.com/CycloneDX/cyclonedx-python/commit/a58ed740fd5f6a603d76a0308d69551a186f8c65))

* chore: update `flake8` to v4 and add `autopep8` (#283)

closes #275

update locked dependencies:
  • Updating pycodestyle (2.7.0 -&gt; 2.8.0)
  • Updating pyflakes (2.3.1 -&gt; 2.4.0)
  • Updating flake8 (3.9.2 -&gt; 4.0.1)
  • Installing autopep8 (1.6.0)
  • Updating flake8-annotations (2.0.1 -&gt; 2.7.0)

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`87aa348`](https://github.com/CycloneDX/cyclonedx-python/commit/87aa3487864ca94cab3c2c9dff3c263f0a849c21))

* chore: Bump mypy from 0.910 to 0.920 (#286)

Bumps [mypy](https://github.com/python/mypy) from 0.910 to 0.920.
- [Release notes](https://github.com/python/mypy/releases)
- [Commits](https://github.com/python/mypy/compare/v0.910...v0.920)

---
updated-dependencies:
- dependency-name: mypy
  dependency-type: direct:development
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`a2dc03f`](https://github.com/CycloneDX/cyclonedx-python/commit/a2dc03f15a994361c973e97f2f9c406a41f9d7cd))

* chore: build(deps): Bump cyclonedx-python-lib from 0.11.1 to 0.12.2 (#282)

Bumps [cyclonedx-python-lib](https://github.com/CycloneDX/cyclonedx-python-lib) from 0.11.1 to 0.12.2.
- [Release notes](https://github.com/CycloneDX/cyclonedx-python-lib/releases)
- [Changelog](https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/CHANGELOG.md)
- [Commits](https://github.com/CycloneDX/cyclonedx-python-lib/compare/v0.11.1...v0.12.2)

---
updated-dependencies:
- dependency-name: cyclonedx-python-lib
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`6b51a66`](https://github.com/CycloneDX/cyclonedx-python/commit/6b51a66094afa5e424d8548724e5d09ea3851f7d))

* chore: remove dev-container (#265)

closes #262

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`16349cb`](https://github.com/CycloneDX/cyclonedx-python/commit/16349cbef449ded638c0fdcba01d3b1a6978678a))

### Documentation

* docs: readme maintenance - shields &amp; links (#266)

* README: added typehint to the vode blocks

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* README: fixed fenced-code and lists

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* README: shields got modernixed and linked

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* README: harmonized links

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a34046f`](https://github.com/CycloneDX/cyclonedx-python/commit/a34046f9b4c96d013fdf2dbdac5e930aa9204e15))

### Feature

* feat: add support for CycloneDX 1.4 specification (#294)

* feat: add support for output to CycloneDX 1.4 (draft)
feat: Error with return code 2 if attempting to output in JSON and SchemaVersion &lt; 1.2
test: Multiple tests added

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* fix: addressed flake8 issues
fix: added missing bump to dependencies

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* fix: corrected import

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* ci: removed poetry cache as broken?

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* bump to latest RC for cyclonedx-python-lib

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* doc: migration to RTD (#296)

* doc: migration to RTD.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* doc: removed references to schema version 1.4

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* doc: updates to include schema version

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* doc: cleanup

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* feat: BREAKING CHANGE - relocated concrete parsers (#299)
BREAKING CHANGE Concrete Parsers now reside in this project, not `cyclonedx-python-lib`

* re-located tests for Utils

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* feat: BREAKING CHANGE - relocated concrete parsers from `cyclonedx-python-lib`
doc: updated to reflect breaking changes
dod: added changelog

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* feat: BREAKING CHANGE - relocated concrete parsers from `cyclonedx-python-lib`
doc: updated to reflect breaking changes
dod: added changelog

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* chore: removed schema validation from unit tests as this is performed in upstream library `cyclonedx-python-lib`

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* chore: removed schema validation from unit tests as this is performed in upstream library `cyclonedx-python-lib`

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* chore: add pre-release manual GH workflow

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;
Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* chore: bump to latest RC of `cyclonedx-python-lib`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* added `purl` into `Component`s output by parsers

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* Ignore type for packageurl imports

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* doc: corrected project title

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt;

* chore: bump to released version of `cyclonedx-python-lib`

Signed-off-by: Paul Horton &lt;paul.horton@owasp.org&gt; ([`7bb6d32`](https://github.com/CycloneDX/cyclonedx-python/commit/7bb6d328adec59cdd4c3ab80eb5f39568ca3bc9c))

### Test

* test: CI/CT for the docker image

CI for the docker image ([`6c4a6de`](https://github.com/CycloneDX/cyclonedx-python/commit/6c4a6deb3293dfaf059d0d114a93b570257e5dfb))

### Unknown

* 1.6.0

Automatically generated by python-semantic-release ([`958af1a`](https://github.com/CycloneDX/cyclonedx-python/commit/958af1af991d1f90644e265ad3862ba76e4a9287))

* doc: migration to RTD (#296)

* doc: migration to RTD.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* doc: removed references to schema version 1.4

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`1744f4d`](https://github.com/CycloneDX/cyclonedx-python/commit/1744f4d77a16e135a26fdf28a5367dd187ad7502))

* Update CONTRIBUTING.md ([`1175c84`](https://github.com/CycloneDX/cyclonedx-python/commit/1175c8433a36ac5c98020e3fb04fe619bf9d994b))

* Merge pull request #279 from CycloneDX/contributing-file

initial CONTRIBUTING file ([`73fcd78`](https://github.com/CycloneDX/cyclonedx-python/commit/73fcd784a003358ec5a6666982cf7ee1e93bc62a))

* initial CONTRIBUTING file

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`104d223`](https://github.com/CycloneDX/cyclonedx-python/commit/104d223fe773abffc7006817d4657c635846a34c))

* gh-action: docker test build

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3b92b00`](https://github.com/CycloneDX/cyclonedx-python/commit/3b92b003cc5a862f72404720da7df601ce6dd457))

* rename python ci workflow

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`b1f57fb`](https://github.com/CycloneDX/cyclonedx-python/commit/b1f57fb378fe2dafcda372c9539ef86f0077ca25))

* CHORE: gh-action release use org&#39;s secrets

as part of #271 ([`71d1c47`](https://github.com/CycloneDX/cyclonedx-python/commit/71d1c47c6de565c20239a79e04229bbe317accb7))

* gh-action release use org&#39;s secrets

as of #271

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`80a6e68`](https://github.com/CycloneDX/cyclonedx-python/commit/80a6e683cbca01b8f2a628b64a5ba58557e575b7))

* CHORE: build(deps-dev): Bump coverage from 6.1.2 to 6.2

build(deps-dev): Bump coverage from 6.1.2 to 6.2 ([`36dd7bd`](https://github.com/CycloneDX/cyclonedx-python/commit/36dd7bdd571f677f04863d904a4dce589b378745))

* CHORE: build(deps-dev): Bump flake8-bugbear from 21.9.2 to 21.11.29

build(deps-dev): Bump flake8-bugbear from 21.9.2 to 21.11.29 ([`c7a5fd0`](https://github.com/CycloneDX/cyclonedx-python/commit/c7a5fd0d8cc4f618ebc988767ced1bb050eeaf07))

* DOCS: fix README shield labels ([`7291d06`](https://github.com/CycloneDX/cyclonedx-python/commit/7291d0604227a09645b5d8807587559191d0874d))


## v1.5.3 (2021-11-23)

### Fix

* fix: revert to previous process for building Docker image as PyPi index update is too slow to pull straight away after publish

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`67bb738`](https://github.com/CycloneDX/cyclonedx-python/commit/67bb738246bfe0ca3acd409d8c5a27fd7a305347))

### Unknown

* 1.5.3

Automatically generated by python-semantic-release ([`ce33cf0`](https://github.com/CycloneDX/cyclonedx-python/commit/ce33cf0217dc087fa970179199a0d9fafb26aec6))

* Merge branch &#39;master&#39; of github.com:CycloneDX/cyclonedx-python ([`186bdda`](https://github.com/CycloneDX/cyclonedx-python/commit/186bddaf940a4292cfa7757f96dbceec5ced829e))


## v1.5.2 (2021-11-23)

### Fix

* fix: corrected docker image build process to not rely on `dist` folder which is cleaned up by python-semantic-release

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`6c65c11`](https://github.com/CycloneDX/cyclonedx-python/commit/6c65c11d439169417e2ef7e94cacb1ec216eb11c))

### Unknown

* 1.5.2

Automatically generated by python-semantic-release ([`7586867`](https://github.com/CycloneDX/cyclonedx-python/commit/7586867d53b3edcf1663705e6b913147da96cd38))


## v1.5.1 (2021-11-23)

### Fix

* fix: Re-enable build and publish of Docker Image (#263)

* fix: update `Dockerfile` to use Python 3.10

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt;

* ci: renable publishing of Docker Images

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`478360d`](https://github.com/CycloneDX/cyclonedx-python/commit/478360db0de269159ab6e3777cd291b87e2e1174))

### Unknown

* 1.5.1

Automatically generated by python-semantic-release ([`dd31888`](https://github.com/CycloneDX/cyclonedx-python/commit/dd31888b0a6b564da3c170437ec92fbe275200d1))


## v1.5.0 (2021-11-17)

### Feature

* feat: support for Python 3.10 (#261)

* enabled py3.10 tests in CI

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* add py-version classifiers

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`f4f9ffe`](https://github.com/CycloneDX/cyclonedx-python/commit/f4f9ffe4b1e2d4fffe4ad0b274a067a20c9c372f))

### Unknown

* 1.5.0

Automatically generated by python-semantic-release ([`31fdd93`](https://github.com/CycloneDX/cyclonedx-python/commit/31fdd930cc500423fa167e0d83a2b070b08bcc76))


## v1.4.3 (2021-11-16)

### Ci

* ci: run release action on push to master

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`24477a0`](https://github.com/CycloneDX/cyclonedx-python/commit/24477a0c30e3ffbc088837b55bcc4336a3d564a1))

### Fix

* fix: add static code analysis, better typing and bump cyclonedx-python-lib to 0.11

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`d5d9f56`](https://github.com/CycloneDX/cyclonedx-python/commit/d5d9f563f2ceb1bdfb2f9cb39ff07af9f0deca26))

### Unknown

* 1.4.3

Automatically generated by python-semantic-release ([`8050477`](https://github.com/CycloneDX/cyclonedx-python/commit/805047778e0c14fce44353659ed34454c9029070))

* FIX: add static code analysis, better typing and bump to `cyclonedx-python-lib` &gt;= `0.11.0`

* fixed some tox issues

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* add more QA

bumped `cyclonedx-python-lib` to the version that opened type-checks
added QA tools: `mypy`, `flake8-annotations`, `flake8-bugbear`

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* gitignore alternative paths of `venv`

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* gh-action CI no longer failes fast

this allowes to run all tests, regardless of failes in parallel tests of the matrix

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* add missing return types

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* make mypy pass

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* tests dont run subprocesses in the shell

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* unittest run in verbose mode

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* fix windows tox run

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt;

* make tests a module

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`3080b57`](https://github.com/CycloneDX/cyclonedx-python/commit/3080b571c2561268d90b0ecee17788da9046893b))


## v1.4.2 (2021-11-12)

### Build

* build(deps-dev): Bump coverage from 6.1.1 to 6.1.2

Bumps [coverage](https://github.com/nedbat/coveragepy) from 6.1.1 to 6.1.2.
- [Release notes](https://github.com/nedbat/coveragepy/releases)
- [Changelog](https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst)
- [Commits](https://github.com/nedbat/coveragepy/compare/6.1.1...6.1.2)

---
updated-dependencies:
- dependency-name: coverage
  dependency-type: direct:development
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`3ce6467`](https://github.com/CycloneDX/cyclonedx-python/commit/3ce64679915a7ab83aa67da05087ca6b4e84c4ef))

* build(deps-dev): Bump coverage from 5.5 to 6.1.1

Bumps [coverage](https://github.com/nedbat/coveragepy) from 5.5 to 6.1.1.
- [Release notes](https://github.com/nedbat/coveragepy/releases)
- [Changelog](https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst)
- [Commits](https://github.com/nedbat/coveragepy/compare/coverage-5.5...6.1.1)

---
updated-dependencies:
- dependency-name: coverage
  dependency-type: direct:development
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`bd63845`](https://github.com/CycloneDX/cyclonedx-python/commit/bd63845c397490e56e2bcd64a7b7e879ef9bc027))

### Fix

* fix: if no input file is supplied and no input is provided on STDIN, we will now try to automatically locate (in the current working directory) a manifest with default name for the input type specified. This works for PIP (Pipfile.lock), Poetry (poetry.lock) and Requirements (requirements.txt)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`93f9e59`](https://github.com/CycloneDX/cyclonedx-python/commit/93f9e5985f0d0cecd865b66119276d33b2175fe9))

### Unknown

* 1.4.2

Automatically generated by python-semantic-release ([`e39ebd3`](https://github.com/CycloneDX/cyclonedx-python/commit/e39ebd34916f0a56028d2b0585ed37e6bbcf59f4))

* Merge pull request #257 from CycloneDX/fix/256-no-default-file-when-no-input-on-stdin

FIX: Fallback to default manifest names in current directory when no `-i` supplied and nothing piped in via STDIN ([`c0f0766`](https://github.com/CycloneDX/cyclonedx-python/commit/c0f07665589db93727db0df90f78b5fc89abb9ab))

* doc: updated documentation

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`47612e6`](https://github.com/CycloneDX/cyclonedx-python/commit/47612e6929684bf0fe57aad5d9cf13c71ff156ef))

* typo corrected

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`4949a0d`](https://github.com/CycloneDX/cyclonedx-python/commit/4949a0df1d8da8ab503b44b5c55540220c79d21d))

* Merge pull request #255 from CycloneDX/dependabot/pip/coverage-6.1.2

build(deps-dev): Bump coverage from 6.1.1 to 6.1.2 ([`6924dac`](https://github.com/CycloneDX/cyclonedx-python/commit/6924dacaf7f288a96f6826262968d21dcd16965e))

* Merge pull request #252 from jkowalleck/patch-1

Create CODEOWNERS ([`b64c707`](https://github.com/CycloneDX/cyclonedx-python/commit/b64c707e9610480f940a95a22505dc39777306f9))

* run github &#34;CI&#34; on commits to master ([`00532dd`](https://github.com/CycloneDX/cyclonedx-python/commit/00532dd0e6265da74832f5000d875e5837d15709))

* Merge pull request #251 from CycloneDX/dependabot/pip/coverage-6.1.1

build(deps-dev): Bump coverage from 5.5 to 6.1.1 ([`525ee0e`](https://github.com/CycloneDX/cyclonedx-python/commit/525ee0eee102d8b97c48f52a5e8d61b2ea786f53))

* Create CODEOWNERS

Signed-off-by: Jan Kowalleck &lt;jan.kowalleck@gmail.com&gt; ([`a29525a`](https://github.com/CycloneDX/cyclonedx-python/commit/a29525a69aeccab0e9eabedf62463487cc9d23a2))


## v1.4.1 (2021-10-26)

### Chore

* chore: manual addition of breaking changes in 1.4.0 into CHANGELOG

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`84fceb2`](https://github.com/CycloneDX/cyclonedx-python/commit/84fceb293aeeef2e716866edd53e589b91ba9340))

### Fix

* fix: corrected documentation after deprecation of `-rf`, `-pf`, `--poetry-file`, `--requirements-file` and `--pip-file`
doc: updated documentation to clarify there is a single input parameter: `-i`

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`4c4c8d8`](https://github.com/CycloneDX/cyclonedx-python/commit/4c4c8d8d4756ebc953c26504052d5469f3c47cfa))

### Unknown

* 1.4.1

Automatically generated by python-semantic-release ([`8f525f2`](https://github.com/CycloneDX/cyclonedx-python/commit/8f525f24c9e91e5b0bad30fe23527ca87abea711))


## v1.4.0 (2021-10-21)

### Feature

* feat: add conda support (bump cyclonedx-python-lib to ^0.10.0)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`cb24275`](https://github.com/CycloneDX/cyclonedx-python/commit/cb24275f3e8716244de2b4ef0a046b879fa88ba5))

### Fix

* fix: encoding issues on Windows (bump cyclonedx-python-lib to ^0.10.2)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`da6772b`](https://github.com/CycloneDX/cyclonedx-python/commit/da6772be89ad923b1d8df6dd3b2a89c6e5805571))

* fix: encoding issues on Windows (bump cyclonedx-python-lib to ^0.10.1)

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`fe5df36`](https://github.com/CycloneDX/cyclonedx-python/commit/fe5df3607157b2f24854ef1f69457f163d79a093))

### Unknown

* 1.4.0

Automatically generated by python-semantic-release ([`564076b`](https://github.com/CycloneDX/cyclonedx-python/commit/564076b3d2c3c140aa7c50c5385e841d9f4d40f6))

* Merge pull request #247 from CycloneDX/feat/conda-support

FEATURE: Add Conda Support ([`c3709af`](https://github.com/CycloneDX/cyclonedx-python/commit/c3709af0fce553ac43809e87bfd5b303dbfdceac))

* fixed some tests

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`002b31d`](https://github.com/CycloneDX/cyclonedx-python/commit/002b31d3a06367f13c433e1e604754e373b2d538))


## v1.3.1 (2021-10-19)

### Fix

* fix: bump to cyclonedx-python-lib to resolve issue #244

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`ebea3ef`](https://github.com/CycloneDX/cyclonedx-python/commit/ebea3ef47e917479a7474489bb274b5fa9704375))

### Unknown

* 1.3.1

Automatically generated by python-semantic-release ([`a030392`](https://github.com/CycloneDX/cyclonedx-python/commit/a030392b751fc2b36f7f892b82806b3cedbbde8a))

* Merge pull request #246 from CycloneDX/feat/add-basic-license-support

fix: bump to cyclonedx-python-lib to resolve issue #244 ([`d831254`](https://github.com/CycloneDX/cyclonedx-python/commit/d8312546ddb94d0e7ac7fce2335ae52f6fc415f0))


## v1.3.0 (2021-10-19)

### Feature

* feat: add license information in CycloneDX BOM when using Environment as the source

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`5d1f9a7`](https://github.com/CycloneDX/cyclonedx-python/commit/5d1f9a76cfa2bc1461a3dcf4c140d81876a37c40))

### Unknown

* 1.3.0

Automatically generated by python-semantic-release ([`8d01377`](https://github.com/CycloneDX/cyclonedx-python/commit/8d013774696d89d8e52ebf81c5539de9c6f4d955))

* Merge pull request #245 from CycloneDX/feat/add-basic-license-support

Add license information in CycloneDX BOM when using Environment as the source ([`26f2500`](https://github.com/CycloneDX/cyclonedx-python/commit/26f25002f380b18e5bbc70460fd50f90d170f965))


## v1.2.0 (2021-10-12)

### Feature

* feat: update to latest stable cyclonedx-python-lib

- Enables PipEnv support natively
- Vast improvements to quality and information contained in the genereated CycloneDX BOM documents - see `cyclonedx-python-lib` for details
- Various old files removes

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`6145bd5`](https://github.com/CycloneDX/cyclonedx-python/commit/6145bd52c450e66f42367e61e086d2a9d9818b47))

### Unknown

* 1.2.0

Automatically generated by python-semantic-release ([`1e46b3d`](https://github.com/CycloneDX/cyclonedx-python/commit/1e46b3d6181b6165e0320e4a1c073e961990bb87))

* Merge pull request #243 from CycloneDX/feat/bump-cyclonedx-lib-0.8.x

Update to latest stable `cyclonedx-python-lib` ([`68f7daa`](https://github.com/CycloneDX/cyclonedx-python/commit/68f7daa50e6d4841c1c27184c370047ff4a29488))


## v1.1.0 (2021-10-04)

### Feature

* feat: add support for generating SBOM from poetry.lock files

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`bb4ac0f`](https://github.com/CycloneDX/cyclonedx-python/commit/bb4ac0f29b46db59b192191f65dfa40757268188))

### Unknown

* 1.1.0

Automatically generated by python-semantic-release ([`ca992f2`](https://github.com/CycloneDX/cyclonedx-python/commit/ca992f29dca21aecd31d9eeb858a966b3ef34315))


## v1.0.5 (2021-09-27)

### Fix

* fix: handle `requirements.txt` which contain dependencies without a version statement and warn that they cannot be included in the resulting CycloneDX BOM

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`e637e56`](https://github.com/CycloneDX/cyclonedx-python/commit/e637e56cada6d841dae193c106647b0b03a4e776))

### Unknown

* 1.0.5

Automatically generated by python-semantic-release ([`5523909`](https://github.com/CycloneDX/cyclonedx-python/commit/552390974ba35f664e5854afcad05fa35270991f))

* Merge pull request #236 from CycloneDX/enhancement/issue-235-requirements-unpinned-versions

fix: handle `requirements.txt` which contain dependencies without a v… ([`f57ab1a`](https://github.com/CycloneDX/cyclonedx-python/commit/f57ab1a0ec14a3ef604058d21dfa59d88f8d462a))


## v1.0.4 (2021-09-27)

### Fix

* fix: error message when `requirements.txt` file is non-existent updated

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`3bbc071`](https://github.com/CycloneDX/cyclonedx-python/commit/3bbc071a1ff26599bd9eb3220de38bd9c58fa294))

### Unknown

* 1.0.4

Automatically generated by python-semantic-release ([`c8b00bc`](https://github.com/CycloneDX/cyclonedx-python/commit/c8b00bc490faa1bd402ed5176daa422516ff8940))

* Merge pull request #234 from CycloneDX/enhancement/issue-232-error-message

fix: error message when `requirements.txt` file is non-existent updated ([`2e6acee`](https://github.com/CycloneDX/cyclonedx-python/commit/2e6acee74bba98d05b03dae61e22149e747946f5))


## v1.0.3 (2021-09-27)

### Build

* build: added flake8 as dev dependency

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`a8fed84`](https://github.com/CycloneDX/cyclonedx-python/commit/a8fed843986d60da49649e6d9393ef77be2e80fa))

* build: updated all dependencies

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`616b949`](https://github.com/CycloneDX/cyclonedx-python/commit/616b949e0d3200cd7c3a3e5131213e2e9bb51cfe))

### Ci

* ci: define missing env variable in CI workflow

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`49db8c2`](https://github.com/CycloneDX/cyclonedx-python/commit/49db8c2c587ab75cdcfb12513a89905b61b6e854))

* ci: updated GitHub workflows to align with those used in cyclonedx-python-lib

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`0b11f5a`](https://github.com/CycloneDX/cyclonedx-python/commit/0b11f5a7d7699a88e0d689f4cc33108a3017f355))

### Fix

* fix: default to &#34;requirements.txt&#34; in current directory when &#34;-r&#34; flag is supplied but not &#34;-rf&#34; flag is supplied

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`bb7e30a`](https://github.com/CycloneDX/cyclonedx-python/commit/bb7e30a869300b1e63a00d7db4bcc7f35d68552d))

### Test

* test: align Tox configuration with cyclonedx-python-lib

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`1e5c6b6`](https://github.com/CycloneDX/cyclonedx-python/commit/1e5c6b61542a1f2b5459ce2f2a84923505e86a1f))

### Unknown

* 1.0.3

Automatically generated by python-semantic-release ([`f3522b9`](https://github.com/CycloneDX/cyclonedx-python/commit/f3522b941f0300d178448f8071ace2b379eb713d))

* Merge pull request #233 from CycloneDX/fix/issue-230-hang-with-no-rf-flag

Fix for hang when no `-rf` flag supplied with `-r` flag ([`651b35f`](https://github.com/CycloneDX/cyclonedx-python/commit/651b35ffb4f70004fff2bc685ccf523d6aa13e16))

* Merge pull request #229 from madpah/fix/bump-dependencies

build: updated all dependencies ([`5587777`](https://github.com/CycloneDX/cyclonedx-python/commit/558777717130ec37d1bf3417b85bfa1819b972bd))


## v1.0.2 (2021-09-13)

### Fix

* fix: Release GH action ([`148421b`](https://github.com/CycloneDX/cyclonedx-python/commit/148421bcd8cea2b5f8f3bd5958f6f7171afe859e))

### Unknown

* 1.0.2

Automatically generated by python-semantic-release ([`5d077a2`](https://github.com/CycloneDX/cyclonedx-python/commit/5d077a220abb50d71ee068f4ca1242c7d722e2dc))


## v1.0.1 (2021-09-13)

### Fix

* fix(ci): corrected main to master branch.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`7162cd9`](https://github.com/CycloneDX/cyclonedx-python/commit/7162cd9385729dafbdc15dbb55e9ac5adf3906cf))

### Unknown

* 1.0.1

Automatically generated by python-semantic-release ([`9af491d`](https://github.com/CycloneDX/cyclonedx-python/commit/9af491d343dc3f3cc45bbd2c72861dd3e2fb2856))

* Merged in master. ([`95b89a7`](https://github.com/CycloneDX/cyclonedx-python/commit/95b89a7a191b57e0720d5e09e396dab6acd506fe))

* fix(ci) - bumped release workflow to run on Python 3.9 which is supported.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`fd7cd8c`](https://github.com/CycloneDX/cyclonedx-python/commit/fd7cd8c4ff9c88a55a540c24cbe7bc14086a1d63))

* Merge pull request #221 from madpah/feature/migrate-to-cyclonedx-python-lib

Migration to new cyclonedx-python-lib for SBOM generation ([`3b1a13c`](https://github.com/CycloneDX/cyclonedx-python/commit/3b1a13c453d4477de0aba9613d9c7f7fba2843cb))

* Corrected Development Status classifier.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`0263610`](https://github.com/CycloneDX/cyclonedx-python/commit/0263610160f86ef9b499682aa848c392bdca2908))

* Removed Python 3.5, added 3.8, 3.9 support in GitLab CI.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`9ecb7b8`](https://github.com/CycloneDX/cyclonedx-python/commit/9ecb7b800b6e059a6459efb58f3f9a88b665fb9c))

* Addressed issues reported by flake8..

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`177a99f`](https://github.com/CycloneDX/cyclonedx-python/commit/177a99f6701cfc9e6c284038d3d9b43d6f16a350))

* Updated documentation.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`ef76b4d`](https://github.com/CycloneDX/cyclonedx-python/commit/ef76b4dedfc59f79eab04fbcbf678b68ca2e877c))

* Started rewrite of tests.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`914463b`](https://github.com/CycloneDX/cyclonedx-python/commit/914463bd2e448b287a4851631d9f9bd9be1b5a7d))

* Fixed a few things:
- Was defaulting to Environment incorrectly
- Output to STDOUT also output to a file named &#39;-&#39;
- Now support data from STDIN

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`4a47efb`](https://github.com/CycloneDX/cyclonedx-python/commit/4a47efbb53cb59bc154b0c5c9067dfb835a440a3))

* Moved from local cyclonedx-python-lib dependency to published version on PyPi.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`3ac87a6`](https://github.com/CycloneDX/cyclonedx-python/commit/3ac87a60c0e885aa3d4b45e1f5849d1a4ac32b2c))

* Re-work to consume new cyclonedx python library which will do all the heavy lifting.

Signed-off-by: Paul Horton &lt;phorton@sonatype.com&gt; ([`25f89fd`](https://github.com/CycloneDX/cyclonedx-python/commit/25f89fde49b2fa982d6beb4bfd5e7b69299b31be))

* Merge pull request #190 from CycloneDX/dependabot/github_actions/actions/setup-python-2.2.2 ([`f5a0946`](https://github.com/CycloneDX/cyclonedx-python/commit/f5a094617f1167f08abdf75946761e24399a522f))

* Merge pull request #191 from CycloneDX/dependabot/github_actions/actions/upload-release-asset-1.0.2 ([`caac584`](https://github.com/CycloneDX/cyclonedx-python/commit/caac5844199406730d9db770089f2d04f0cef18c))

* Merge pull request #192 from CycloneDX/dependabot/github_actions/actions/create-release-1.1.4

Bump actions/create-release from 1 to 1.1.4 ([`33e47b0`](https://github.com/CycloneDX/cyclonedx-python/commit/33e47b0bbaf83582a60ed090d2eb1b0bb45a7a6e))

* Merge pull request #202 from CycloneDX/dependabot/docker/python-3.9.6-slim-buster

Bump python from 3.9.5-slim-buster to 3.9.6-slim-buster ([`c859cb7`](https://github.com/CycloneDX/cyclonedx-python/commit/c859cb7542ea0ba726ee91191a3a83c311739b10))

* Merge pull request #206 from mgrajesh1/issue_205_pypi_connect_using_proxy

Issue# 205. Use HTTPS_PROXY if env is set ([`f5108c4`](https://github.com/CycloneDX/cyclonedx-python/commit/f5108c469f2e53fbbb8c33f449d19cb9967e72da))

* Updating copyright statements ([`18e206e`](https://github.com/CycloneDX/cyclonedx-python/commit/18e206e4ebb7eaeaf9d764a5e539e4ec28f27e4d))

* Issue# 205. Use HTTPS_PROXY if env is set

Signed-off-by: akshadpai &lt;akshadpai01@gmail.com&gt; ([`4fb8714`](https://github.com/CycloneDX/cyclonedx-python/commit/4fb87148ea71d7d2b777442568e0f5b43bb892da))

* Bump python from 3.9.5-slim-buster to 3.9.6-slim-buster

Bumps python from 3.9.5-slim-buster to 3.9.6-slim-buster.

---
updated-dependencies:
- dependency-name: python
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`ecd0fba`](https://github.com/CycloneDX/cyclonedx-python/commit/ecd0fbaf14c93e372c2fdf5d7c86cd4f4fd8f168))

* Added notice and updated file headers ([`0f4ff74`](https://github.com/CycloneDX/cyclonedx-python/commit/0f4ff74890fd30c81e5cec6d17470fedb771ae09))

* Bump actions/create-release from 1 to 1.1.4

Bumps [actions/create-release](https://github.com/actions/create-release) from 1 to 1.1.4.
- [Release notes](https://github.com/actions/create-release/releases)
- [Commits](https://github.com/actions/create-release/compare/v1...v1.1.4)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`6371988`](https://github.com/CycloneDX/cyclonedx-python/commit/63719884de0c76e25a7977c2fdb7378d27dd3b22))

* Bump actions/upload-release-asset from 1 to 1.0.2

Bumps [actions/upload-release-asset](https://github.com/actions/upload-release-asset) from 1 to 1.0.2.
- [Release notes](https://github.com/actions/upload-release-asset/releases)
- [Commits](https://github.com/actions/upload-release-asset/compare/v1...v1.0.2)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`50cfad3`](https://github.com/CycloneDX/cyclonedx-python/commit/50cfad3d7863c595d577561c51a8759eca3deb1b))

* Bump actions/setup-python from 2.2.1 to 2.2.2

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 2.2.1 to 2.2.2.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/v2.2.1...v2.2.2)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`dbca5da`](https://github.com/CycloneDX/cyclonedx-python/commit/dbca5dac176ce3d69d45df831bfc268ee4c2de25))

* Merge pull request #186 from CycloneDX/dependabot/docker/python-3.9.5-slim-buster

Bump python from 3.9.2-slim-buster to 3.9.5-slim-buster ([`3cd645a`](https://github.com/CycloneDX/cyclonedx-python/commit/3cd645a9b74f4e7921cd53ab336c286280b10c47))

* Bump python from 3.9.2-slim-buster to 3.9.5-slim-buster

Bumps python from 3.9.2-slim-buster to 3.9.5-slim-buster.

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`657b1ff`](https://github.com/CycloneDX/cyclonedx-python/commit/657b1ff16c8928b02f0e0929a85662af3d44001e))

* Merge pull request #173 from CycloneDX/dependabot/pip/packageurl-python-0.9.4

Bump packageurl-python from 0.9.3 to 0.9.4 ([`1615d91`](https://github.com/CycloneDX/cyclonedx-python/commit/1615d91436cd9bc68f26d5e69085133adb953834))

* Merge pull request #165 from CycloneDX/dependabot/docker/python-3.9.2-slim-buster

Bump python from 3.9.1-slim-buster to 3.9.2-slim-buster ([`4a33cf1`](https://github.com/CycloneDX/cyclonedx-python/commit/4a33cf117388456329e89e139ea876b1e13269b1))

* Bump packageurl-python from 0.9.3 to 0.9.4

Bumps [packageurl-python](https://github.com/package-url/packageurl-python) from 0.9.3 to 0.9.4.
- [Release notes](https://github.com/package-url/packageurl-python/releases)
- [Changelog](https://github.com/package-url/packageurl-python/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/package-url/packageurl-python/compare/v0.9.3...0.9.4)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`7f153fa`](https://github.com/CycloneDX/cyclonedx-python/commit/7f153faf7c4ba63949734502fdc1bb6eddb13edb))

* Merge pull request #161 from CycloneDX/dependabot/pip/packaging-20.9

Bump packaging from 20.7 to 20.9 ([`57a0b16`](https://github.com/CycloneDX/cyclonedx-python/commit/57a0b168b2043235e48593d61aa9120d285e6bda))

* Bump python from 3.9.1-slim-buster to 3.9.2-slim-buster

Bumps python from 3.9.1-slim-buster to 3.9.2-slim-buster.

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`fba5248`](https://github.com/CycloneDX/cyclonedx-python/commit/fba524838a6d388bf429dacac53b5ff51351d657))

* Bump packaging from 20.7 to 20.9

Bumps [packaging](https://github.com/pypa/packaging) from 20.7 to 20.9.
- [Release notes](https://github.com/pypa/packaging/releases)
- [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/pypa/packaging/compare/20.7...20.9)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`240847f`](https://github.com/CycloneDX/cyclonedx-python/commit/240847f340db80ba3c967d7a1cf59cff841968e9))

* Merge pull request #149 from CycloneDX/dependabot/github_actions/actions/setup-python-v2.2.1

Bump actions/setup-python from v2.2.0 to v2.2.1 ([`5eb87ee`](https://github.com/CycloneDX/cyclonedx-python/commit/5eb87ee0ab403b5673bd38baea63bcfb31c230af))

* Bump actions/setup-python from v2.2.0 to v2.2.1

Bumps [actions/setup-python](https://github.com/actions/setup-python) from v2.2.0 to v2.2.1.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/v2.2.0...3105fb18c05ddd93efea5f9e0bef7a03a6e9e7df)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`3c9eaae`](https://github.com/CycloneDX/cyclonedx-python/commit/3c9eaae3babb5cdce00d1a3192e7e02f9023d8fe))

* Merge pull request #147 from CycloneDX/dependabot/github_actions/actions/setup-python-v2.2.0

Bump actions/setup-python from v2.1.4 to v2.2.0 ([`a31103e`](https://github.com/CycloneDX/cyclonedx-python/commit/a31103e7351e45e354d5edb6d1b332c904381b08))

* Bump actions/setup-python from v2.1.4 to v2.2.0

Bumps [actions/setup-python](https://github.com/actions/setup-python) from v2.1.4 to v2.2.0.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/v2.1.4...8c5ea631b2b2d5d8840cf4a2b183a8a0edc1e40d)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`89dacb0`](https://github.com/CycloneDX/cyclonedx-python/commit/89dacb0e1e95b975251597465e54e56ea4b9ccbb))

* Merge pull request #142 from CycloneDX/dependabot/docker/python-3.9.1-slim-buster

Bump python from 3.9.0-slim-buster to 3.9.1-slim-buster ([`2f1f5ba`](https://github.com/CycloneDX/cyclonedx-python/commit/2f1f5ba215b72147be425a0a51360674ed9ebfe1))

* Bump python from 3.9.0-slim-buster to 3.9.1-slim-buster

Bumps python from 3.9.0-slim-buster to 3.9.1-slim-buster.

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`37eaf19`](https://github.com/CycloneDX/cyclonedx-python/commit/37eaf19ef115e715af2314e68da1c6df222749d0))


## v0.4.3 (2020-12-05)

### Unknown

* Bug fix release - invalid XML character handling ([`0d5c01e`](https://github.com/CycloneDX/cyclonedx-python/commit/0d5c01e616f6c716c9f261eed9d45f52d9644d9f))

* Merge pull request #140 from CycloneDX/invalid-xml-characters

Fix for invalid xml characters ([`8de9c16`](https://github.com/CycloneDX/cyclonedx-python/commit/8de9c16741605f54e57caae15e91dbddd74682ed))

* Re-order test data ([`c8fa641`](https://github.com/CycloneDX/cyclonedx-python/commit/c8fa641ee8a41aae885f2650427c522270d81067))

* Add handling for invalid xml characters ([`228af8d`](https://github.com/CycloneDX/cyclonedx-python/commit/228af8dda7a6421aa66801a0e8a153dabffd9ca9))

* Add test for invalid xml unicode characters ([`56bbb40`](https://github.com/CycloneDX/cyclonedx-python/commit/56bbb40fe53bea4111b74d0564477305cca0053d))

* Merge pull request #138 from CycloneDX/dependabot/pip/packaging-20.7

Bump packaging from 20.4 to 20.7 ([`ca4cf86`](https://github.com/CycloneDX/cyclonedx-python/commit/ca4cf86ccd109d112fa5d234139564a6ed99a55e))

* Bump packaging from 20.4 to 20.7

Bumps [packaging](https://github.com/pypa/packaging) from 20.4 to 20.7.
- [Release notes](https://github.com/pypa/packaging/releases)
- [Changelog](https://github.com/pypa/packaging/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/pypa/packaging/compare/20.4...20.7)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`0ce786c`](https://github.com/CycloneDX/cyclonedx-python/commit/0ce786cfbe4ce41f22c10dbda112a242c36e1fe3))

* Merge pull request #137 from CycloneDX/dependabot/pip/requests-2.25.0

Bump requests from 2.24.0 to 2.25.0 ([`e943788`](https://github.com/CycloneDX/cyclonedx-python/commit/e943788f5321c1bc292de531b77560590d02d5c1))

* Bump requests from 2.24.0 to 2.25.0

Bumps [requests](https://github.com/psf/requests) from 2.24.0 to 2.25.0.
- [Release notes](https://github.com/psf/requests/releases)
- [Changelog](https://github.com/psf/requests/blob/master/HISTORY.md)
- [Commits](https://github.com/psf/requests/compare/v2.24.0...v2.25.0)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`5b22ddf`](https://github.com/CycloneDX/cyclonedx-python/commit/5b22ddfecd8f0ccde335458756a99c0ea5477e33))

* Merge pull request #134 from CycloneDX/dependabot/github_actions/actions/checkout-v2.3.4

Bump actions/checkout from v2.3.3 to v2.3.4 ([`85bb4fc`](https://github.com/CycloneDX/cyclonedx-python/commit/85bb4fcabb5dadf188332d3d04c38565fc62bf10))

* Bump actions/checkout from v2.3.3 to v2.3.4

Bumps [actions/checkout](https://github.com/actions/checkout) from v2.3.3 to v2.3.4.
- [Release notes](https://github.com/actions/checkout/releases)
- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
- [Commits](https://github.com/actions/checkout/compare/v2.3.3...5a4ac9002d0be2fb38bd78e4b4dbde5606d7042f)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`22b9305`](https://github.com/CycloneDX/cyclonedx-python/commit/22b9305f76a59699edc3d13c320bf7c5944e8488))

* Merge pull request #132 from CycloneDX/dependabot/pip/setuptools-50.3.2

Bump setuptools from 50.3.1 to 50.3.2 ([`d01d920`](https://github.com/CycloneDX/cyclonedx-python/commit/d01d9204289ff27f589331b2c6d4e284ab3eff00))

* Bump setuptools from 50.3.1 to 50.3.2

Bumps [setuptools](https://github.com/pypa/setuptools) from 50.3.1 to 50.3.2.
- [Release notes](https://github.com/pypa/setuptools/releases)
- [Changelog](https://github.com/pypa/setuptools/blob/master/CHANGES.rst)
- [Commits](https://github.com/pypa/setuptools/compare/v50.3.1...v50.3.2)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`e2df914`](https://github.com/CycloneDX/cyclonedx-python/commit/e2df914e5b5ae6076d2b449117ab0f513b7fd0f9))

* Merge pull request #133 from CycloneDX/dependabot/pip/pytest-6.1.2

Bump pytest from 6.1.1 to 6.1.2 ([`140a00a`](https://github.com/CycloneDX/cyclonedx-python/commit/140a00a4e932ea5cf059e4dfc02b502b4a5b757b))

* Bump pytest from 6.1.1 to 6.1.2

Bumps [pytest](https://github.com/pytest-dev/pytest) from 6.1.1 to 6.1.2.
- [Release notes](https://github.com/pytest-dev/pytest/releases)
- [Changelog](https://github.com/pytest-dev/pytest/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/pytest-dev/pytest/compare/6.1.1...6.1.2)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`bf5267d`](https://github.com/CycloneDX/cyclonedx-python/commit/bf5267d1f85d83cbde310510afcc54fa043e0267))

* Merge pull request #127 from CycloneDX/dependabot/pip/setuptools-50.3.1

Bump setuptools from 50.3.0 to 50.3.1 ([`bb69861`](https://github.com/CycloneDX/cyclonedx-python/commit/bb69861b200704ec04145b202633c468677d9403))

* Merge pull request #128 from CycloneDX/dependabot/github_actions/actions/setup-python-v2.1.4

Bump actions/setup-python from v2.1.3 to v2.1.4 ([`de9da36`](https://github.com/CycloneDX/cyclonedx-python/commit/de9da36e48c3fa43b3601297499d7d1a72c5799f))

* Bump actions/setup-python from v2.1.3 to v2.1.4

Bumps [actions/setup-python](https://github.com/actions/setup-python) from v2.1.3 to v2.1.4.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/v2.1.3...41b7212b1668f5de9d65e9c82aa777e6bbedb3a8)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`765d9d1`](https://github.com/CycloneDX/cyclonedx-python/commit/765d9d124536d58b7a6a93d518e9375e161644dd))

* Bump setuptools from 50.3.0 to 50.3.1

Bumps [setuptools](https://github.com/pypa/setuptools) from 50.3.0 to 50.3.1.
- [Release notes](https://github.com/pypa/setuptools/releases)
- [Changelog](https://github.com/pypa/setuptools/blob/master/CHANGES.rst)
- [Commits](https://github.com/pypa/setuptools/compare/v50.3.0...v50.3.1)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`162d7ea`](https://github.com/CycloneDX/cyclonedx-python/commit/162d7ea960048a7b1e0e793558467d7fb1403cf2))

* Merge pull request #126 from CycloneDX/devcontainer

Add devcontainer configuration ([`859e9a4`](https://github.com/CycloneDX/cyclonedx-python/commit/859e9a476127adc90a15b461ca9a88cf6a64810f))

* Add devcontainer configuration ([`b9c34a6`](https://github.com/CycloneDX/cyclonedx-python/commit/b9c34a67030208cc7204889ecfd48e007ca3d242))

* Merge pull request #118 from c0d3nh4ck/master

Added support for metadata timestamp ([`d954df8`](https://github.com/CycloneDX/cyclonedx-python/commit/d954df868d155f58daa690c6f567e660fe3900d1))

* check for metadata to be empty ([`180f207`](https://github.com/CycloneDX/cyclonedx-python/commit/180f20714ced7a64a256f12f3c9ecf2d047427d4))


## v0.4.2 (2020-10-08)

### Unknown

* Maintenance release ([`308f98e`](https://github.com/CycloneDX/cyclonedx-python/commit/308f98efe11c404f414676e256e50d733153dc26))

* Merge pull request #121 from CycloneDX/dependabot/docker/python-3.9.0-slim-buster

Bump python from 3.8.6-slim-buster to 3.9.0-slim-buster ([`7703a52`](https://github.com/CycloneDX/cyclonedx-python/commit/7703a52b8fd342392d1836c30f89d575f1183490))

* Merge pull request #120 from CycloneDX/dependabot/pip/packageurl-python-0.9.3

Bump packageurl-python from 0.9.2 to 0.9.3 ([`257fa2b`](https://github.com/CycloneDX/cyclonedx-python/commit/257fa2b539980350838368dbdf54476f528f6107))

* Bump python from 3.8.6-slim-buster to 3.9.0-slim-buster

Bumps python from 3.8.6-slim-buster to 3.9.0-slim-buster.

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`bf938c9`](https://github.com/CycloneDX/cyclonedx-python/commit/bf938c9a0ebfe983f5914ae604ab4894592ceac8))

* Bump packageurl-python from 0.9.2 to 0.9.3

Bumps [packageurl-python](https://github.com/package-url/packageurl-python) from 0.9.2 to 0.9.3.
- [Release notes](https://github.com/package-url/packageurl-python/releases)
- [Changelog](https://github.com/package-url/packageurl-python/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/package-url/packageurl-python/compare/v0.9.2...v0.9.3)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`1a7d36b`](https://github.com/CycloneDX/cyclonedx-python/commit/1a7d36bb44337fd13d7afb6be87fcd7159bf48a5))

* Merge pull request #119 from CycloneDX/dependabot/pip/pytest-6.1.1

Bump pytest from 6.1.0 to 6.1.1 ([`202f029`](https://github.com/CycloneDX/cyclonedx-python/commit/202f0290124241d60dfb9d3cf3e25e928546cc6c))

* Bump pytest from 6.1.0 to 6.1.1

Bumps [pytest](https://github.com/pytest-dev/pytest) from 6.1.0 to 6.1.1.
- [Release notes](https://github.com/pytest-dev/pytest/releases)
- [Changelog](https://github.com/pytest-dev/pytest/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/pytest-dev/pytest/compare/6.1.0...6.1.1)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`005f85f`](https://github.com/CycloneDX/cyclonedx-python/commit/005f85fb6e7590174abb358b52ceb16639baa74d))

* update for the xml part to convert metadata to dictionary object ([`d31e8b2`](https://github.com/CycloneDX/cyclonedx-python/commit/d31e8b269afa93aaaa87c2bf0999f018aa94c2cf))

* updated metadata to dictionary from list ([`deebd3d`](https://github.com/CycloneDX/cyclonedx-python/commit/deebd3d38e8f2c3697b8be20de05788706ec89cb))

* Added code to check for metadata value ([`a3497fd`](https://github.com/CycloneDX/cyclonedx-python/commit/a3497fd5370b1cb289fbf0a82ece65cca0808dd7))

* added default value for metadata as None ([`86641b6`](https://github.com/CycloneDX/cyclonedx-python/commit/86641b6196a8e823f53f4554caaf2ceb4a32b486))

* Added support for metadata timestamp ([`27eb3e5`](https://github.com/CycloneDX/cyclonedx-python/commit/27eb3e550fceeb2e737f602048c5ccf6b9d95664))

* Merge pull request #116 from CycloneDX/dependabot/github_actions/actions/setup-python-v2.1.3

Bump actions/setup-python from v2.1.2 to v2.1.3 ([`e7c1cd9`](https://github.com/CycloneDX/cyclonedx-python/commit/e7c1cd9fa6a564b015d923b2219509bab9804cd1))

* Bump actions/setup-python from v2.1.2 to v2.1.3

Bumps [actions/setup-python](https://github.com/actions/setup-python) from v2.1.2 to v2.1.3.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/v2.1.2...c181ffa198a1248f902bc2f7965d2f9a36c2d7f6)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`648ab6f`](https://github.com/CycloneDX/cyclonedx-python/commit/648ab6fd6b4d0f2f374ebf8d563352101024e474))

* Merge pull request #112 from CycloneDX/dependabot/pip/xmlschema-1.2.5

Bump xmlschema from 1.2.4 to 1.2.5 ([`9f22abf`](https://github.com/CycloneDX/cyclonedx-python/commit/9f22abff2d65b9787f980277622463af10a0e68a))

* Merge pull request #113 from CycloneDX/dependabot/pip/pytest-6.1.0

Bump pytest from 6.0.1 to 6.1.0 ([`5801185`](https://github.com/CycloneDX/cyclonedx-python/commit/58011858ad080cb47fcc967ce47c8a421578f195))

* Merge pull request #115 from praveenmylavarapu/make-component-generic

Make component type generic ([`584e929`](https://github.com/CycloneDX/cyclonedx-python/commit/584e929ab97e5b82d4738568cc2ba0f8543c670f))

* Merge pull request #114 from praveenmylavarapu/remove-duplicate

remove duplicate function call ([`7ad5892`](https://github.com/CycloneDX/cyclonedx-python/commit/7ad5892cd958719323b3ef047b06b99bdea458ee))

* Make component type generic ([`4a2d220`](https://github.com/CycloneDX/cyclonedx-python/commit/4a2d220f3c7d7bd2af663977cde93faae20ab8d4))

* remove duplicate function call ([`df6d6d0`](https://github.com/CycloneDX/cyclonedx-python/commit/df6d6d035649f765672c2ddb67de08257a6594f3))

* Bump pytest from 6.0.1 to 6.1.0

Bumps [pytest](https://github.com/pytest-dev/pytest) from 6.0.1 to 6.1.0.
- [Release notes](https://github.com/pytest-dev/pytest/releases)
- [Changelog](https://github.com/pytest-dev/pytest/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/pytest-dev/pytest/compare/6.0.1...6.1.0)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`f8ffeeb`](https://github.com/CycloneDX/cyclonedx-python/commit/f8ffeebb97c58fc79eacbf2f58a8f90fdf6260bd))

* Bump xmlschema from 1.2.4 to 1.2.5

Bumps [xmlschema](https://github.com/brunato/xmlschema) from 1.2.4 to 1.2.5.
- [Release notes](https://github.com/brunato/xmlschema/releases)
- [Changelog](https://github.com/sissaschool/xmlschema/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/brunato/xmlschema/compare/v1.2.4...v1.2.5)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`8f94c58`](https://github.com/CycloneDX/cyclonedx-python/commit/8f94c589b8d756c13a3c26cc2662681d0933391e))

* Revert &#34;Bump pytest from 6.0.1 to 6.0.2&#34;

This reverts commit 986d2ef737e051be04203b14ee5d11b26b00edb7. ([`528341a`](https://github.com/CycloneDX/cyclonedx-python/commit/528341af07dc7a4cdee995432b652aee8c6100e7))

* Merge pull request #108 from CycloneDX/dependabot/pip/pytest-6.0.2

Bump pytest from 6.0.1 to 6.0.2 ([`feed962`](https://github.com/CycloneDX/cyclonedx-python/commit/feed962319f1dc0e47e24ec7ef603228602a55bf))

* Bump pytest from 6.0.1 to 6.0.2

Bumps [pytest](https://github.com/pytest-dev/pytest) from 6.0.1 to 6.0.2.
- [Release notes](https://github.com/pytest-dev/pytest/releases)
- [Changelog](https://github.com/pytest-dev/pytest/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/pytest-dev/pytest/compare/6.0.1...6.0.2)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`986d2ef`](https://github.com/CycloneDX/cyclonedx-python/commit/986d2ef737e051be04203b14ee5d11b26b00edb7))

* Merge pull request #109 from CycloneDX/dependabot/pip/packageurl-python-0.9.2

Bump packageurl-python from 0.9.1 to 0.9.2 ([`bfa1db6`](https://github.com/CycloneDX/cyclonedx-python/commit/bfa1db63790938e038a6ceb52ca1281a01362818))

* Bump packageurl-python from 0.9.1 to 0.9.2

Bumps [packageurl-python](https://github.com/package-url/packageurl-python) from 0.9.1 to 0.9.2.
- [Release notes](https://github.com/package-url/packageurl-python/releases)
- [Changelog](https://github.com/package-url/packageurl-python/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/package-url/packageurl-python/compare/v0.9.1...v0.9.2)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`a2a3596`](https://github.com/CycloneDX/cyclonedx-python/commit/a2a35968f8b8e0580b3bfbd0cd2a14ea2110b7b5))

* Merge pull request #107 from CycloneDX/dependabot/pip/xmlschema-1.2.4

Bump xmlschema from 1.2.3 to 1.2.4 ([`c58a756`](https://github.com/CycloneDX/cyclonedx-python/commit/c58a7565c8299db469b6f37c87557e1357bbb927))

* Merge pull request #111 from CycloneDX/dependabot/docker/python-3.8.6-slim-buster

Bump python from 3.8.5-slim-buster to 3.8.6-slim-buster ([`00eccf6`](https://github.com/CycloneDX/cyclonedx-python/commit/00eccf61b9b9de2a7fa01d496764f60c48ce43c5))

* Bump python from 3.8.5-slim-buster to 3.8.6-slim-buster

Bumps python from 3.8.5-slim-buster to 3.8.6-slim-buster.

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`0db21cd`](https://github.com/CycloneDX/cyclonedx-python/commit/0db21cd5dad63c689636228694e8c5ed9dc6b923))

* Merge pull request #110 from CycloneDX/dependabot/github_actions/actions/checkout-v2.3.3

Bump actions/checkout from v2.3.2 to v2.3.3 ([`f84ace1`](https://github.com/CycloneDX/cyclonedx-python/commit/f84ace1dde38b794c81cda88dbf6d6a5f23abd61))

* Bump actions/checkout from v2.3.2 to v2.3.3

Bumps [actions/checkout](https://github.com/actions/checkout) from v2.3.2 to v2.3.3.
- [Release notes](https://github.com/actions/checkout/releases)
- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
- [Commits](https://github.com/actions/checkout/compare/v2.3.2...a81bbbf8298c0fa03ea29cdc473d45769f953675)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`f1381a5`](https://github.com/CycloneDX/cyclonedx-python/commit/f1381a51978f00c5f7eb7fa1c72e0a28649f3704))

* Bump xmlschema from 1.2.3 to 1.2.4

Bumps [xmlschema](https://github.com/brunato/xmlschema) from 1.2.3 to 1.2.4.
- [Release notes](https://github.com/brunato/xmlschema/releases)
- [Changelog](https://github.com/sissaschool/xmlschema/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/brunato/xmlschema/compare/v1.2.3...v1.2.4)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`8a92d37`](https://github.com/CycloneDX/cyclonedx-python/commit/8a92d370eb4ec3655066bb1c736542c5cd636f66))

* Merge pull request #101 from CycloneDX/dependabot/docker/python-3.8.5-slim-buster

Bump python from 3.8.1-slim-buster to 3.8.5-slim-buster ([`bfa41d2`](https://github.com/CycloneDX/cyclonedx-python/commit/bfa41d2830231b94a8885f2db5bd02b57ed5f9f0))

* Merge pull request #105 from CycloneDX/null-license-handling

Add test data for package with a null license ([`50e634b`](https://github.com/CycloneDX/cyclonedx-python/commit/50e634bfb741d9d273aeba298f590368791ca5ad))

* Fix test data for GitHub runners

There is something odd here that needs more investigation to make it more deterministic. ([`d2fee97`](https://github.com/CycloneDX/cyclonedx-python/commit/d2fee97a6557410eebe257039bca19aeda32884c))

* Merge branch &#39;master&#39; into null-license-handling ([`0d11a2e`](https://github.com/CycloneDX/cyclonedx-python/commit/0d11a2e247700467a91d09a5ce03e1928547a6c5))

* Add test data for package with a null license ([`9958abb`](https://github.com/CycloneDX/cyclonedx-python/commit/9958abbf679f9cc19249675d5c218f6106f6402b))


## v0.4.1 (2020-09-08)

### Unknown

* Bug fix release

- Fix handling of null licenses
- Fix Docker image bundled tool version ([`ab588be`](https://github.com/CycloneDX/cyclonedx-python/commit/ab588be864ac0d14f3ddfbf5ecb93f019967a561))

* Merge pull request #104 from rback123/patch-103

Prevent crash when package_license is none from pypi null value ([`57e31f0`](https://github.com/CycloneDX/cyclonedx-python/commit/57e31f03193d22fc508e1c9f68a2993cb12d0aa3))

* Added NoneType check for package_license ([`6b18250`](https://github.com/CycloneDX/cyclonedx-python/commit/6b182500ddf055ac702716d05f15307c41a82f21))

* Bump python from 3.8.1-slim-buster to 3.8.5-slim-buster

Bumps python from 3.8.1-slim-buster to 3.8.5-slim-buster.

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`a5e46d1`](https://github.com/CycloneDX/cyclonedx-python/commit/a5e46d1dde1d82136fa8ec3bf901b5570c7786da))

* Merge pull request #102 from CycloneDX/docker-release-fix

Use release built package when building Docker image ([`3c8b583`](https://github.com/CycloneDX/cyclonedx-python/commit/3c8b583b20b388aef996d2dcce15eb205106e093))

* Install locally created package when creating Docker image ([`890bdee`](https://github.com/CycloneDX/cyclonedx-python/commit/890bdeed11f686ef666d2d649373ac18c9645cd7))

* Merge pull request #100 from CycloneDX/dependabot/github_actions/actions/setup-python-v2.1.2

Bump actions/setup-python from v1 to v2.1.2 ([`60ecc7c`](https://github.com/CycloneDX/cyclonedx-python/commit/60ecc7c91e646e9504b7b48dfc926b6f52455472))

* Bump actions/setup-python from v1 to v2.1.2

Bumps [actions/setup-python](https://github.com/actions/setup-python) from v1 to v2.1.2.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/v1...24156c231c5e9d581bde27d0cdbb72715060ea51)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`6d34eaa`](https://github.com/CycloneDX/cyclonedx-python/commit/6d34eaa5b8abecebd38d27bd4d0c0159747e4f5e))

* Merge pull request #99 from CycloneDX/dependabot/github_actions/actions/checkout-v2.3.2

Bump actions/checkout from v1 to v2.3.2 ([`dc2af31`](https://github.com/CycloneDX/cyclonedx-python/commit/dc2af313ae60e81d8689a5e65612363387e414a7))

* Bump actions/checkout from v1 to v2.3.2

Bumps [actions/checkout](https://github.com/actions/checkout) from v1 to v2.3.2.
- [Release notes](https://github.com/actions/checkout/releases)
- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
- [Commits](https://github.com/actions/checkout/compare/v1...2036a08e25fa78bbd946711a407b529a0a1204bf)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`127e885`](https://github.com/CycloneDX/cyclonedx-python/commit/127e8851dec86f21c285187eb9f4f7e756b43b3e))

* Merge pull request #98 from davidkarlsen/dependabot

fix language definition ([`6cc7a17`](https://github.com/CycloneDX/cyclonedx-python/commit/6cc7a1795f81eb9891f8feeee378490e733dbb81))

* fix language definition ([`cee1611`](https://github.com/CycloneDX/cyclonedx-python/commit/cee16114b785f6ce7e47d533ba860fe1eda35a31))

* Merge pull request #97 from davidkarlsen/dependabot

Configure dependabot through config-files ([`003e20c`](https://github.com/CycloneDX/cyclonedx-python/commit/003e20c29f5b62c673bbd7dd8ab53e6c67bf833c))

* Configure dependabot through config-files

Signed-off-by: David Karlsen &lt;david@davidkarlsen.com&gt; ([`36c92f7`](https://github.com/CycloneDX/cyclonedx-python/commit/36c92f712e20ef783eb5e34c564da4fece5b0cea))

* Merge pull request #96 from CycloneDX/dependabot/pip/setuptools-50.3.0

Bump setuptools from 50.1.0 to 50.3.0 ([`2727ff9`](https://github.com/CycloneDX/cyclonedx-python/commit/2727ff9faa41b673733b59f5c3368b0dfaa6e1dc))

* Bump setuptools from 50.1.0 to 50.3.0

Bumps [setuptools](https://github.com/pypa/setuptools) from 50.1.0 to 50.3.0.
- [Release notes](https://github.com/pypa/setuptools/releases)
- [Changelog](https://github.com/pypa/setuptools/blob/master/CHANGES.rst)
- [Commits](https://github.com/pypa/setuptools/compare/v50.1.0...v50.3.0)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`60e3547`](https://github.com/CycloneDX/cyclonedx-python/commit/60e35478ac04e12f4bd8cf8ec085bb2774a171d0))

* Add additional comments/doco to the GitHub workflows ([`f49bad6`](https://github.com/CycloneDX/cyclonedx-python/commit/f49bad60e60c748d357322720d49985dd00ccb90))

* Merge pull request #93 from CycloneDX/dependabot/pip/setuptools-50.1.0

Bump setuptools from 18.5 to 50.1.0 ([`de6c3a9`](https://github.com/CycloneDX/cyclonedx-python/commit/de6c3a933e89ac00b195aef801a1932b14efa669))

* Bump setuptools from 18.5 to 50.1.0

Bumps [setuptools](https://github.com/pypa/setuptools) from 18.5 to 50.1.0.
- [Release notes](https://github.com/pypa/setuptools/releases)
- [Changelog](https://github.com/pypa/setuptools/blob/master/CHANGES.rst)
- [Commits](https://github.com/pypa/setuptools/compare/18.5...v50.1.0)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`b9dd248`](https://github.com/CycloneDX/cyclonedx-python/commit/b9dd2484af195bd928ba3f19f097e2a2a96dfff2))

* Merge pull request #84 from CycloneDX/dependabot/pip/packageurl-python-0.9.1

Bump packageurl-python from 0.8.7 to 0.9.1 ([`1434bd8`](https://github.com/CycloneDX/cyclonedx-python/commit/1434bd867c341e44151f4bd29f330eed628ea25d))

* Bump packageurl-python from 0.8.7 to 0.9.1

Bumps [packageurl-python](https://github.com/package-url/packageurl-python) from 0.8.7 to 0.9.1.
- [Release notes](https://github.com/package-url/packageurl-python/releases)
- [Changelog](https://github.com/package-url/packageurl-python/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/package-url/packageurl-python/compare/v0.8.7...v0.9.1)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`c45e7b7`](https://github.com/CycloneDX/cyclonedx-python/commit/c45e7b70214a07e2241f1af76a01498954617562))

* Add 30 minute timeout for GitHub workflows ([`47341f7`](https://github.com/CycloneDX/cyclonedx-python/commit/47341f7661b5d2a4b99c3544e248664853798af2))

* Merge pull request #68 from CycloneDX/dependabot/pip/packaging-20.4

Bump packaging from 19.2 to 20.4 ([`9123452`](https://github.com/CycloneDX/cyclonedx-python/commit/9123452d842d0975a6a3874fef10f1d6f9359114))

* Bump packaging from 19.2 to 20.4

Bumps [packaging](https://github.com/pypa/packaging) from 19.2 to 20.4.
- [Release notes](https://github.com/pypa/packaging/releases)
- [Changelog](https://github.com/pypa/packaging/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/pypa/packaging/compare/19.2...20.4)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`cc0ba25`](https://github.com/CycloneDX/cyclonedx-python/commit/cc0ba25e0b60aea91ab4b7a7abdd73d8b17640f7))

* Merge pull request #82 from CycloneDX/dependabot/pip/pytest-6.0.1

Bump pytest from 4.6.9 to 6.0.1 ([`ab1eb35`](https://github.com/CycloneDX/cyclonedx-python/commit/ab1eb358946e5c602ebd47a1b8e0849e102622df))

* Merge pull request #78 from CycloneDX/dependabot/pip/requests-2.24.0

Bump requests from 2.22.0 to 2.24.0 ([`ac5ab88`](https://github.com/CycloneDX/cyclonedx-python/commit/ac5ab88111a6c332294aa245ae1fc2d19127405b))

* Bump requests from 2.22.0 to 2.24.0

Bumps [requests](https://github.com/psf/requests) from 2.22.0 to 2.24.0.
- [Release notes](https://github.com/psf/requests/releases)
- [Changelog](https://github.com/psf/requests/blob/master/HISTORY.md)
- [Commits](https://github.com/psf/requests/compare/v2.22.0...v2.24.0)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`53ed092`](https://github.com/CycloneDX/cyclonedx-python/commit/53ed092fe00296d413fe89c712b43d397f3538d9))

* Merge pull request #89 from CycloneDX/dependabot/pip/xmlschema-1.2.3

Bump xmlschema from 1.0.16 to 1.2.3 ([`72cad92`](https://github.com/CycloneDX/cyclonedx-python/commit/72cad929f6f8e83c1b3baaedc2027f6ccbb2ef35))

* Bump xmlschema from 1.0.16 to 1.2.3

Bumps [xmlschema](https://github.com/brunato/xmlschema) from 1.0.16 to 1.2.3.
- [Release notes](https://github.com/brunato/xmlschema/releases)
- [Changelog](https://github.com/sissaschool/xmlschema/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/brunato/xmlschema/compare/v1.0.16...v1.2.3)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`2e0aa9f`](https://github.com/CycloneDX/cyclonedx-python/commit/2e0aa9f546b4240fe44433ed6bccd8cd16ab3806))


## v0.4.0 (2020-09-03)

### Unknown

* Fix incorrect twine upload repo ([`2ad67fe`](https://github.com/CycloneDX/cyclonedx-python/commit/2ad67fe4150450aab7d0448a2b33cb119887178d))

* Feature release

- add JSON support
- include schema files in package
- code quality improvements ([`74cdcaf`](https://github.com/CycloneDX/cyclonedx-python/commit/74cdcaf2d4e08d95a78801dcda80d0e95574a912))

* Remove manual release script ([`927da78`](https://github.com/CycloneDX/cyclonedx-python/commit/927da786a0fa3021738a591db8c0ba7529aa21f5))

* Add Docker image and GitHub release to workflow ([`4f921a8`](https://github.com/CycloneDX/cyclonedx-python/commit/4f921a8b1608ce2f6b8f15e94a6d12d970217dfd))

* Add docker build and push to release workflow ([`7b868dc`](https://github.com/CycloneDX/cyclonedx-python/commit/7b868dcce7507675b7b657def7af9f92ea939bc9))

* Merge branch &#39;master&#39; into github-workflows ([`6134a9b`](https://github.com/CycloneDX/cyclonedx-python/commit/6134a9b7821b1a464313b799f22eab9927d95bc2))

* Merge pull request #94 from CycloneDX/github-workflows

GitHub workflow for releases ([`aa84147`](https://github.com/CycloneDX/cyclonedx-python/commit/aa841471e0d6ddd68c414fefbc5c32710bd06a3a))

* Add release workflow ([`9396ba8`](https://github.com/CycloneDX/cyclonedx-python/commit/9396ba819714c5174f50ad76988a54e05efcf159))

* Remove newline from VERSION ([`c67b398`](https://github.com/CycloneDX/cyclonedx-python/commit/c67b3982ada361aa83c8a881b3be504a54b6ead0))

* Run CI tests on Ubuntu, Windows and Mac agents ([`eb84c46`](https://github.com/CycloneDX/cyclonedx-python/commit/eb84c46fe59f24337fef3237f6af45e10520c638))

* Rename pythonpackge workflow file to ci ([`2137711`](https://github.com/CycloneDX/cyclonedx-python/commit/21377112e327e3bb7e8d6d372c9dc1f88cc5bf9f))

* Bump pytest from 4.6.9 to 6.0.1

Bumps [pytest](https://github.com/pytest-dev/pytest) from 4.6.9 to 6.0.1.
- [Release notes](https://github.com/pytest-dev/pytest/releases)
- [Changelog](https://github.com/pytest-dev/pytest/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/pytest-dev/pytest/compare/4.6.9...6.0.1)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`a3db165`](https://github.com/CycloneDX/cyclonedx-python/commit/a3db165660415220956ef372c5c4d2ce0e84863f))

* Merge pull request #63 from coderpatros/json

Support for JSON output ([`a71084c`](https://github.com/CycloneDX/cyclonedx-python/commit/a71084cd851fc3a40e9dc322281796200b32e05d))

* Replace snapshot JSON schema with final v1.2 schema ([`44ad74b`](https://github.com/CycloneDX/cyclonedx-python/commit/44ad74be1db17d39f9ea82834b65be21f44951c9))

* Update existing tests to use CLI instead of module imports ([`99430cc`](https://github.com/CycloneDX/cyclonedx-python/commit/99430cc51b1d80c8949e4518dab5341e05b053ca))

* Add initial &#34;preview&#34; JSON output support ([`44e0667`](https://github.com/CycloneDX/cyclonedx-python/commit/44e0667b57d52da3861e17071bcfe9f6fefe0f47))

* Fix bug that can result in duplicate components being included in the BOM ([`5fd04f5`](https://github.com/CycloneDX/cyclonedx-python/commit/5fd04f5550b12c88589d43eb9064c30d56b415ab))

* Refactor to use Component, Hash and License classes and rename some XML methods

This is in preparation for supporting JSON output. ([`3be896a`](https://github.com/CycloneDX/cyclonedx-python/commit/3be896afdb0d4b205b27d222f22e37c7a2fcb02e))

* Fix path issue when debugging from virtual environment ([`d208b16`](https://github.com/CycloneDX/cyclonedx-python/commit/d208b16bb0a4d9bac65556d57f4cbc44b5b93db5))

* Git ignore files in build/ and dist/ ([`d80b959`](https://github.com/CycloneDX/cyclonedx-python/commit/d80b959647aa6dbcbcc77d6c19b044686abf38c0))

* Merge pull request #55 from coderpatros/tests

Add a basic happy path test ([`c373dad`](https://github.com/CycloneDX/cyclonedx-python/commit/c373dad3f068354cc3af85d5a7d8e8afce2b3fbf))

* Include xml schema files in package ([`0ae93d6`](https://github.com/CycloneDX/cyclonedx-python/commit/0ae93d6b35d41d87a11e933316c20b75924727ce))

* Merge remote-tracking branch &#39;refs/remotes/origin/master&#39;

Conflicts:
	cyclonedx/cli/generateBom.py

Changes to generateBom.py moved to reader.py ([`ab307e5`](https://github.com/CycloneDX/cyclonedx-python/commit/ab307e50ac0ad536ff2690534001062c56707d2c))

* Merge pull request #59 from RobertMaaskant/pypi-mirror-support

Pypi mirror support ([`169b642`](https://github.com/CycloneDX/cyclonedx-python/commit/169b6428283361292dd90ef3fdf5abdb55542350))

* Use OrderedDict for hashes to fix failing test under Python 3.5

The dictionary implementation was changed from version 3.6. This means
generated output is different under Python 3.5 ([`518cae9`](https://github.com/CycloneDX/cyclonedx-python/commit/518cae97316040fffcf9971845b1b1730e6e353e))

* Fixup for mirror support ([`d53a5d1`](https://github.com/CycloneDX/cyclonedx-python/commit/d53a5d102961245d985ac0e482be70573bca7f4d))

* Fixup of bad refactoring ([`af95c39`](https://github.com/CycloneDX/cyclonedx-python/commit/af95c393f88d59e0814b280ce1f852d8331e316c))

* Refactor + add package info mirror support ([`4876f41`](https://github.com/CycloneDX/cyclonedx-python/commit/4876f4192649ad7d2d5185af937e516b56d63a96))

* Simplified populate_digests method ([`b9c5e0a`](https://github.com/CycloneDX/cyclonedx-python/commit/b9c5e0ac74d8747f9f93a070be5ead7592d58d22))

* Refactor bom building ([`5043e85`](https://github.com/CycloneDX/cyclonedx-python/commit/5043e85c15ec6b7809fd566010a495165dad29ab))

* Prevent main client from running on import ([`d3ce0c7`](https://github.com/CycloneDX/cyclonedx-python/commit/d3ce0c7141c74514a4e58105c0510bca14ef8676))

* Reorder imports ([`19f47b9`](https://github.com/CycloneDX/cyclonedx-python/commit/19f47b9dac021393895891219048dc94f78747cc))

* Remove deprecated python 2.7 from build ([`3791c94`](https://github.com/CycloneDX/cyclonedx-python/commit/3791c94be9c1bfef7c912485485de6e4c0a3bdd2))

* Add basic bom generation test ([`1018f4c`](https://github.com/CycloneDX/cyclonedx-python/commit/1018f4c9f9ea2201bdb021a283f2a7fe90108867))

* Make read_bom importable from cyclonedx.cli ([`421258f`](https://github.com/CycloneDX/cyclonedx-python/commit/421258f50b05cfcab010a911eac26088e0cfd423))

* Use script relative paths for setup.py reference files ([`b06a628`](https://github.com/CycloneDX/cyclonedx-python/commit/b06a6284e6fe578af6459e516f124b98b7a502c6))

* Add create-virtualenv.sh helper script ([`cf8f68b`](https://github.com/CycloneDX/cyclonedx-python/commit/cf8f68b6361a47e7a65f0a27cf12cf40b3f41238))

* Add .gitignore ([`d07d736`](https://github.com/CycloneDX/cyclonedx-python/commit/d07d7360f5e54d9605a9e29b5965f557e7183402))

* Added Slack badge ([`f975a73`](https://github.com/CycloneDX/cyclonedx-python/commit/f975a730cc09ba3cddff48b23e0c83cf53e35e2a))

* Update README.rst ([`c845183`](https://github.com/CycloneDX/cyclonedx-python/commit/c84518396d5759f6395bef5a26f11a5021e804fe))

* Update README.rst ([`f089c23`](https://github.com/CycloneDX/cyclonedx-python/commit/f089c23360d2d5bc712a29337d15f85ffcb3c4d2))

* Update README.rst ([`7cc8e37`](https://github.com/CycloneDX/cyclonedx-python/commit/7cc8e37e4c8fe819c58276e0b8ce62cf02e8eb91))

* Added docker deployment on release ([`6ce0123`](https://github.com/CycloneDX/cyclonedx-python/commit/6ce0123056a6b2ea48fe61b7231f07d554808e09))

* Merge pull request #46 from davidkarlsen/feature/dockerimage

Docker image. Fixes #45 ([`fbf1482`](https://github.com/CycloneDX/cyclonedx-python/commit/fbf148242b967a05da7c170933a195823331ec48))

* Docker image. Fixes #45

Signed-off-by: David Karlsen &lt;david@davidkarlsen.com&gt; ([`7b06b3a`](https://github.com/CycloneDX/cyclonedx-python/commit/7b06b3a9604a27fb5995632cb2305e0942de6389))

* bump ([`0364312`](https://github.com/CycloneDX/cyclonedx-python/commit/0364312d0629ed1b189922a73a3ff126f47c73e9))


## v0.3.5 (2019-12-05)

### Unknown

* bump ([`85b4755`](https://github.com/CycloneDX/cyclonedx-python/commit/85b475551e8225f15d5e48e9c601055f081d6727))


## v0.3.4 (2019-12-05)

### Unknown

* call python ([`0d7ceca`](https://github.com/CycloneDX/cyclonedx-python/commit/0d7ceca561b14692896c9d039b67f58dd69314d0))

* #11 #34 - Fix for version comparison ([`eeaca97`](https://github.com/CycloneDX/cyclonedx-python/commit/eeaca970dfafbf3defd72846b7e4e9616b386cc9))

* Merge pull request #16 from CycloneDX/dependabot/pip/requirements-parser-0.2.0

Bump requirements-parser from 0.1.0 to 0.2.0 ([`5ac8aa0`](https://github.com/CycloneDX/cyclonedx-python/commit/5ac8aa01df9512df671d18377acd10ee6a410860))

* Bump requirements-parser from 0.1.0 to 0.2.0

Bumps [requirements-parser](https://github.com/davidfischer/requirements-parser) from 0.1.0 to 0.2.0.
- [Release notes](https://github.com/davidfischer/requirements-parser/releases)
- [Changelog](https://github.com/davidfischer/requirements-parser/blob/master/docs/changelog.rst)
- [Commits](https://github.com/davidfischer/requirements-parser/compare/v0.1.0...v0.2.0)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`1505aa1`](https://github.com/CycloneDX/cyclonedx-python/commit/1505aa17d05644798c717d4ef3b4967f042da4b4))

* Merge pull request #19 from CycloneDX/dependabot/pip/packaging-19.2

Bump packaging from 19.1 to 19.2 ([`f4a558f`](https://github.com/CycloneDX/cyclonedx-python/commit/f4a558f5e72a80bd99ed5009c091c452473043e2))

* Merge pull request #30 from CycloneDX/dependabot/pip/xmlschema-1.0.16

Bump xmlschema from 1.0.14 to 1.0.16 ([`b22762a`](https://github.com/CycloneDX/cyclonedx-python/commit/b22762ad4ec86b2e496fbe7c44278fbcede3ffdd))

* Merge remote-tracking branch &#39;origin/master&#39; ([`3dba3a4`](https://github.com/CycloneDX/cyclonedx-python/commit/3dba3a4560b084dccbc278241a091fc119f161e9))

* Changed lang ([`b586534`](https://github.com/CycloneDX/cyclonedx-python/commit/b5865342c2290b1a97e4075f2b46e4b7b93a1a9a))

* Merge pull request #4 from msander/patch-1

Continue with other requirements ([`88193b2`](https://github.com/CycloneDX/cyclonedx-python/commit/88193b244b632dd468e0cffe1dd3c815256b03ef))

* Bump xmlschema from 1.0.14 to 1.0.16

Bumps [xmlschema](https://github.com/brunato/xmlschema) from 1.0.14 to 1.0.16.
- [Release notes](https://github.com/brunato/xmlschema/releases)
- [Changelog](https://github.com/sissaschool/xmlschema/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/brunato/xmlschema/compare/v1.0.14...v1.0.16)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`575595c`](https://github.com/CycloneDX/cyclonedx-python/commit/575595cbfb95ac347776b04db935307fa7ba9ffa))

* Update pythonpackage.yml ([`21990bc`](https://github.com/CycloneDX/cyclonedx-python/commit/21990bc2ac03df93ef31f393bd992345b44f06a6))

* bump ([`f795b97`](https://github.com/CycloneDX/cyclonedx-python/commit/f795b978f5359b71b32089c0ec11c505b3e2c9b1))


## v0.3.3 (2019-11-14)

### Unknown

* Updating release process ([`2d47de4`](https://github.com/CycloneDX/cyclonedx-python/commit/2d47de4974ba5c4feac4aaab03bba4cb6cca2e95))

* Merge pull request #29 from llamahunter/patch-1

Support requirements.txt with local files ([`f476f4f`](https://github.com/CycloneDX/cyclonedx-python/commit/f476f4fd7060bf3fc4784c7c7d1d2ea59c027b09))

* Support requirements.txt with local files

It&#39;s possible for the requirements.txt file to have local file listings.  These do not have &#39;name&#39; values, and so cause a runtime error when trying to concatenate a NoneType with a string.  Test for &#39;local_file&#39; requirements and skip them when generating bom.
See https://requirements-parser.readthedocs.io/en/latest/usage.html#parsing-requirement-specifiers ([`97d0cde`](https://github.com/CycloneDX/cyclonedx-python/commit/97d0cdebc4f3895bb5f2304c9ae9da931082bf4b))

* Update README.rst ([`89b488b`](https://github.com/CycloneDX/cyclonedx-python/commit/89b488b2f0e08c5368b26ab7352cace98598404d))

* Update pythonpackage.yml ([`86d1451`](https://github.com/CycloneDX/cyclonedx-python/commit/86d1451cf63bd66bbcb278200432b0b816b5842f))

* Update pythonpackage.yml ([`5db4810`](https://github.com/CycloneDX/cyclonedx-python/commit/5db481048459af2d179b5ebd8f83c0b3263f5ce7))

* migrating from travis-ci to github actions ([`29d989e`](https://github.com/CycloneDX/cyclonedx-python/commit/29d989eea5c7316b8adad2d9e7f6df07bd28fc05))

* Update README.rst ([`a1aa609`](https://github.com/CycloneDX/cyclonedx-python/commit/a1aa609744be72a11eb646344c36bbb5d7668be8))

* Update pythonpackage.yml ([`1cb93bf`](https://github.com/CycloneDX/cyclonedx-python/commit/1cb93bf550d83e39c71be88bf94a37732d08b168))

* Update pythonpackage.yml ([`b9386aa`](https://github.com/CycloneDX/cyclonedx-python/commit/b9386aae2e7544c3ab7e7acf0e27ee4bd49e0786))

* Update pythonpackage.yml ([`c9dc482`](https://github.com/CycloneDX/cyclonedx-python/commit/c9dc4820af8ccb9bcf0bc4831d8eb73765cf3196))

* Update pythonpackage.yml ([`3416ee8`](https://github.com/CycloneDX/cyclonedx-python/commit/3416ee8e55e8771fe6a2acb0b27824c5928d5585))

* bump ([`e84e29f`](https://github.com/CycloneDX/cyclonedx-python/commit/e84e29fa421282da542597016548051f42314da8))

* Bump packaging from 19.1 to 19.2

Bumps [packaging](https://github.com/pypa/packaging) from 19.1 to 19.2.
- [Release notes](https://github.com/pypa/packaging/releases)
- [Changelog](https://github.com/pypa/packaging/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/pypa/packaging/compare/19.1...19.2)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`99ad2cb`](https://github.com/CycloneDX/cyclonedx-python/commit/99ad2cb9c257d1f1b02ddaecd1933b80282742ed))

* Fixes requirements ([`79993b7`](https://github.com/CycloneDX/cyclonedx-python/commit/79993b7a37c1ec0fd6280756d249fe61863a2972))

* Merge pull request #21 from tngraf/master

Encoding detection added ([`a41d616`](https://github.com/CycloneDX/cyclonedx-python/commit/a41d6166310a1fbc8b3295bc7938b3c28eb62af2))

* Encoding detection added ([`938374a`](https://github.com/CycloneDX/cyclonedx-python/commit/938374a6f2ee5541785130bac74f01ce4d72c7df))

* Merge pull request #18 from TTMaZa/TTMaZa-UTF-8-CLI

Enforced UTF-8 encoding while writing bom.xml ([`b3944a1`](https://github.com/CycloneDX/cyclonedx-python/commit/b3944a1f0d62e0c68ed52cdf20fec9988a9981b3))

* Enforced UTF-8 encoding while writing bom.xml ([`2478bf1`](https://github.com/CycloneDX/cyclonedx-python/commit/2478bf1f180898e2d2bc368d056eaf31168620e2))

* Merge pull request #17 from CycloneDX/dependabot/pip/packaging-19.1

Bump packaging from 19.0 to 19.1 ([`cd0ff73`](https://github.com/CycloneDX/cyclonedx-python/commit/cd0ff737e23ff0df3866fb2a241961dd9c96763f))

* Bump packaging from 19.0 to 19.1

Bumps [packaging](https://github.com/pypa/packaging) from 19.0 to 19.1.
- [Release notes](https://github.com/pypa/packaging/releases)
- [Changelog](https://github.com/pypa/packaging/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/pypa/packaging/compare/19.0...19.1)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`b0a2719`](https://github.com/CycloneDX/cyclonedx-python/commit/b0a27192a02aa6f9249eeb73429647a5360626bc))

* Merge pull request #14 from CycloneDX/dependabot/pip/requests-2.22.0

Bump requests from 2.20.1 to 2.22.0 ([`973a89f`](https://github.com/CycloneDX/cyclonedx-python/commit/973a89fd73e128b762d56d69393438e19a8e3fe5))

* Bump requests from 2.20.1 to 2.22.0

Bumps [requests](https://github.com/requests/requests) from 2.20.1 to 2.22.0.
- [Release notes](https://github.com/requests/requests/releases)
- [Changelog](https://github.com/psf/requests/blob/master/HISTORY.md)
- [Commits](https://github.com/requests/requests/compare/v2.20.1...v2.22.0)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`ad3169d`](https://github.com/CycloneDX/cyclonedx-python/commit/ad3169de516b22a316dbc5e655eb4f978a1db3fd))

* Merge pull request #15 from CycloneDX/dependabot/pip/packageurl-python-0.8.7

Bump packageurl-python from 0.8.1 to 0.8.7 ([`324d6a0`](https://github.com/CycloneDX/cyclonedx-python/commit/324d6a06941d96bfae5446f57b993f67057804f4))

* Bump packageurl-python from 0.8.1 to 0.8.7

Bumps [packageurl-python](https://github.com/package-url/packageurl-python) from 0.8.1 to 0.8.7.
- [Release notes](https://github.com/package-url/packageurl-python/releases)
- [Commits](https://github.com/package-url/packageurl-python/compare/v0.8.1...v0.8.7)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`c47b17e`](https://github.com/CycloneDX/cyclonedx-python/commit/c47b17e038352b1b224ca4ca2d5c8ccc232db933))

* Merge pull request #12 from CycloneDX/dependabot/pip/xmlschema-1.0.14

Bump xmlschema from 1.0.7 to 1.0.14 ([`e747f9f`](https://github.com/CycloneDX/cyclonedx-python/commit/e747f9fd642b4ca62bb1dec408902ed2b5bfec46))

* Bump xmlschema from 1.0.7 to 1.0.14

Bumps [xmlschema](https://github.com/brunato/xmlschema) from 1.0.7 to 1.0.14.
- [Release notes](https://github.com/brunato/xmlschema/releases)
- [Changelog](https://github.com/sissaschool/xmlschema/blob/master/CHANGELOG.rst)
- [Commits](https://github.com/brunato/xmlschema/compare/v1.0.7...v1.0.14)

Signed-off-by: dependabot-preview[bot] &lt;support@dependabot.com&gt; ([`4159f7b`](https://github.com/CycloneDX/cyclonedx-python/commit/4159f7bf2ae9c6ce0d17390ea25542583c8dfc12))

* Continue with other requirements

Currently the BOM generation breaks when a single requirement does not refer to a specific version. It would be better to continue with the other requirements. ([`c633e4f`](https://github.com/CycloneDX/cyclonedx-python/commit/c633e4ff02adca28d223247242065393832e4abd))

* Update README.rst ([`b4a1dc0`](https://github.com/CycloneDX/cyclonedx-python/commit/b4a1dc07f2c164d30512f72cb3cc5a798c17c4ee))

* version bump. Added xml pretty printing ([`83cbb7a`](https://github.com/CycloneDX/cyclonedx-python/commit/83cbb7a0f4f9d4669eb12b5812ac2509865cac78))

* Merge pull request #10 from emnetag/patch-08-19

Handle package versions not found in PyPi ([`5d12795`](https://github.com/CycloneDX/cyclonedx-python/commit/5d12795265e9481c3dce856a6d463e30419019d7))

* Handle packages not found in PyPi

If a package version is not found in PyPi, create an entry
for that version and print a warning to the console. ([`2fbb145`](https://github.com/CycloneDX/cyclonedx-python/commit/2fbb1451d6a55268cc3e61fe70d3ac20859cff10))

* Updating SPDX license list to v3.6 ([`51a1727`](https://github.com/CycloneDX/cyclonedx-python/commit/51a17274d913cc08c1b55014dda6b7151436d321))

* Adding release script ([`f2a486d`](https://github.com/CycloneDX/cyclonedx-python/commit/f2a486dbf7ce0e6e065ffd7a18e42cc0fdbdfc48))

* Added topics ([`7bbc751`](https://github.com/CycloneDX/cyclonedx-python/commit/7bbc7519d3d72a397117cb12bb8041bd3af9b64e))

* version bump ([`aa16564`](https://github.com/CycloneDX/cyclonedx-python/commit/aa16564fc3df4720a62b7e39cc474a8acb9bf5ab))

* Updating SPDX license list to v3.5 ([`ddb11b7`](https://github.com/CycloneDX/cyclonedx-python/commit/ddb11b70055f8d10ad21e19ca2fba144bf76cf7b))

* Merge pull request #8 from rback123/patch-6

Support PEP 440 concepts like pre, post, and development versions ([`20d6c5d`](https://github.com/CycloneDX/cyclonedx-python/commit/20d6c5d845d5cc2cf59381972ea036f7c7a2cd99))

* Support PEP 440 concepts like pre, post, and development versioning schemes. ([`4344b9a`](https://github.com/CycloneDX/cyclonedx-python/commit/4344b9a365af391707463c58052de4a3dca3081b))

* Merge pull request #5 from msander/patch-2

Add &#39;requests&#39; requirement to install_requires ([`e026932`](https://github.com/CycloneDX/cyclonedx-python/commit/e02693200188d59b4c3c046a80643094e39ded2f))

* Merge pull request #1 from jhermann/stdin-as-input

Support `-i -` (read from stdin) ([`e5356ef`](https://github.com/CycloneDX/cyclonedx-python/commit/e5356ef69757113913216e2e711f640fc0bbb60e))

* Add &#39;requests&#39; requirement to install_requires ([`625b5a3`](https://github.com/CycloneDX/cyclonedx-python/commit/625b5a33bf1bdd92399c755cd728b34ed4ea5e2d))

* main: support &#39;-i -&#39; (read from stdin)

This allows to call...

    pip freeze | cyclonedx-py -i - ([`e8522a6`](https://github.com/CycloneDX/cyclonedx-python/commit/e8522a679ebd11d151970c26eabf411bd232a881))

* main: output guarded by context ([`e634cb8`](https://github.com/CycloneDX/cyclonedx-python/commit/e634cb876f166e5ccc91d88c1410dc3b3d4f4ea3))

* setup: set +x flag ([`4a1c0d6`](https://github.com/CycloneDX/cyclonedx-python/commit/4a1c0d6317491226c088971342ae92501bd2bed3))

* consolidated main ([`967ca09`](https://github.com/CycloneDX/cyclonedx-python/commit/967ca099ecd06e2c4b48d13e143db47b79975628))

* bump ([`273c3fc`](https://github.com/CycloneDX/cyclonedx-python/commit/273c3fce34bb3837118fbe85b8eb52a6a7c66d28))

* Moved to cli package. Fixed requirements and setup issues. Fixed issue with req not having a version when parsed. ([`4624657`](https://github.com/CycloneDX/cyclonedx-python/commit/4624657bab30afed78fa09b2c8d98b9c5554c8f3))

* Removed unneeded requires entry ([`c857ba8`](https://github.com/CycloneDX/cyclonedx-python/commit/c857ba8abfff4be7fe22737663b4386ababdc8b3))

* corrected keywords ([`7e39138`](https://github.com/CycloneDX/cyclonedx-python/commit/7e39138a62d3af7f193405037a782a99c639b22a))

* corrected dependency name - version bump ([`3f2cb11`](https://github.com/CycloneDX/cyclonedx-python/commit/3f2cb113b3d2db3f5735d5a6df4e8660ddf58226))

* correcting publish ([`635a329`](https://github.com/CycloneDX/cyclonedx-python/commit/635a32935f351f44de2bde2c9affc5398eea5435))

* formatting ([`2dc1b65`](https://github.com/CycloneDX/cyclonedx-python/commit/2dc1b65e5623f962dace3462b02a526bb310e4ef))

* formatting ([`fcd2f00`](https://github.com/CycloneDX/cyclonedx-python/commit/fcd2f00e15156492f6cb8c1c65c138788ccca167))

* formatting ([`fb166d0`](https://github.com/CycloneDX/cyclonedx-python/commit/fb166d09aa751ab3681325d3c46372bb6bacc7d8))

* mods ([`d584ef6`](https://github.com/CycloneDX/cyclonedx-python/commit/d584ef61851fb99fccecefbeeb7f5b0af2d5927e))

* mods ([`9a524a2`](https://github.com/CycloneDX/cyclonedx-python/commit/9a524a2ace698e04ce8203744ac0cc7ddf98aaac))

* mods ([`e4e3950`](https://github.com/CycloneDX/cyclonedx-python/commit/e4e3950faece8cb78218f9d7a19011158e22b6a9))

* Added hashes ([`21d0fd0`](https://github.com/CycloneDX/cyclonedx-python/commit/21d0fd02c45a5982b7bacaf37448f57e664002fd))

* Added bom validation after generation ([`273b828`](https://github.com/CycloneDX/cyclonedx-python/commit/273b828b45894de184875706cd90312710dcc8ca))

* Added bom validation after generation ([`2d82ac0`](https://github.com/CycloneDX/cyclonedx-python/commit/2d82ac0fb558b28d922d0be62b7c9653fea1d887))

* Added keywords and project url ([`818498a`](https://github.com/CycloneDX/cyclonedx-python/commit/818498a28e756b792373b1aca8d86ea043d7ee17))

* Adding Python 3.5 test ([`74807e4`](https://github.com/CycloneDX/cyclonedx-python/commit/74807e4f0a19376d1ae93d661594e74b5fb3f0ab))

* Added bdist_wheel ([`6bf71f7`](https://github.com/CycloneDX/cyclonedx-python/commit/6bf71f784a8ecb7c0b54cc6a185ae275c3d37479))

* removed comment ([`173056e`](https://github.com/CycloneDX/cyclonedx-python/commit/173056e1ad0b6640e29a81b4f1980ab07ef5689b))

* headers ([`128a260`](https://github.com/CycloneDX/cyclonedx-python/commit/128a260b6796b5c711d25b2f2eefa909f2ac96dc))

* Updated cli args and readme ([`c02b7b6`](https://github.com/CycloneDX/cyclonedx-python/commit/c02b7b6f8816a36fdeac2cd8e32ae3981540b5ec))

* Initial commit ([`cc233b7`](https://github.com/CycloneDX/cyclonedx-python/commit/cc233b7e9c256e28bef7a7c20e20c5ade96eb67d))

* Initial commit ([`b9e62ba`](https://github.com/CycloneDX/cyclonedx-python/commit/b9e62bab8e4ec7eac1f81329395b68519bc62bbe))

* Initial commit ([`57bb85f`](https://github.com/CycloneDX/cyclonedx-python/commit/57bb85f310df938dfb09a5c120e6c98a54ea6f7b))
