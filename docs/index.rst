.. # Licensed under the Apache License, Version 2.0 (the "License");
   # you may not use this file except in compliance with the License.
   # You may obtain a copy of the License at
   #
   #     http://www.apache.org/licenses/LICENSE-2.0
   #
   # Unless required by applicable law or agreed to in writing, software
   # distributed under the License is distributed on an "AS IS" BASIS,
   # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   # See the License for the specific language governing permissions and
   # limitations under the License.
   #
   # SPDX-License-Identifier: Apache-2.0

CycloneDX SBOM Generation Tool for Python
=========================================

This project provides a runnable Python-based application
for generating Software Bill of material (SBOM) documents in `CycloneDX`_ format
from:

* Python (virtual) environment
* `Poetry`_ manifest
* `Pipenv`_ manifest
* Pip's `requirements file format`_ format
* `Conda`_ as a Package Manager is no longer supported since version 4.
  However, ``conda``'s Python environments are fully supported via the methods listed above.

The SBOM will contain an aggregate of all your project's dependencies, or those defined by the manifest you supply.

`CycloneDX`_ is a full-stack SBOM specification that is easily created, human-readable, and simple to parse.

.. _CycloneDX: https://cyclonedx.org/
.. _Poetry: https://python-poetry.org/
.. _Pipenv: https://pipenv.pypa.io/
.. _requirements file format: https://pip.pypa.io/en/stable/reference/requirements-file-format/
.. _conda: https://conda.io/

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   usage
   support
   changelog
