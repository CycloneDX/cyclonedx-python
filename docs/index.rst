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

=========================================
CycloneDX SBOM Generation Tool for Python
=========================================

This tool generates Software Bill of material (SBOM) documents in OWASP `CycloneDX`_ format.

Supported data sources are:

* Python (virtual) environment
* `Poetry`_ manifest and lockfile
* `Pipenv`_ manifest and lockfile
* Pip's `requirements file format`_ format
* `PDM`_ manifest and lockfile support is not implemented, yet.
  However, PDM's Python virtual environments are fully supported.
  See the :doc:`docs </usage>` for an example.
* `Conda`_ as a package manager is no longer supported since version 4.
  However, conda's Python environments are fully supported via the methods listed above.
  See the :doc:`docs </usage>` for an example.

Based on `OWASP Software Component Verification Standard for Software Bill of Materials <https://scvs.owasp.org/scvs/v2-software-bill-of-materials/>`_'s
criteria, this tool is capable of producing SBOM documents almost passing Level-2 (only signing needs to be done externally).

The resulting SBOM documents follow `official specifications and standards <https://github.com/CycloneDX/specification>`_,
and might have properties following the Namespace Taxonomies
`cdx:python <https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/python.md>`_,
`cdx:pipenv <https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/pipenv.md>`_,
`cdx:poetry <https://github.com/CycloneDX/cyclonedx-property-taxonomy/blob/main/cdx/poetry.md>`_.

.. _CycloneDX: https://cyclonedx.org/
.. _Poetry: https://python-poetry.org/
.. _Pipenv: https://pipenv.pypa.io/
.. _requirements file format: https://pip.pypa.io/en/stable/reference/requirements-file-format/
.. _PDM: https://pdm-project.org/
.. _Conda: https://conda.io/

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   usage
   contributing
   support
   Changelog <changelog>
   upgrading
