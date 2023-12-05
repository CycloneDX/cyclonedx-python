# This file is part of CycloneDX Python Lib
#
# Licensed under the Apache License, Version 2.0 (the "License");
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
# Copyright (c) OWASP Foundation. All Rights Reserved.


from typing import Any

from cyclonedx.model import ExternalReference, ExternalReferenceType, Tool, XsUri
from cyclonedx.model.bom import Bom

from cyclonedx_py import __version__


def make_bom(**kwargs: Any) -> Bom:
    bom = Bom(**kwargs)
    bom.metadata.tools.add(Tool(
        vendor='CycloneDX',
        name='cyclonedx-bom',
        version=__version__ or 'UNKNOWN',
        external_references=[
            ExternalReference(
                type=ExternalReferenceType.BUILD_SYSTEM,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python/actions')
            ),
            ExternalReference(
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri('https://pypi.org/project/cyclonedx-bom/')
            ),
            ExternalReference(
                type=ExternalReferenceType.DOCUMENTATION,
                url=XsUri('https://cyclonedx-bom-tool.readthedocs.io/')
            ),
            ExternalReference(
                type=ExternalReferenceType.ISSUE_TRACKER,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python/issues')
            ),
            ExternalReference(
                type=ExternalReferenceType.LICENSE,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python/blob/main/LICENSE')
            ),
            ExternalReference(
                type=ExternalReferenceType.RELEASE_NOTES,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python/blob/main/CHANGELOG.md')
            ),
            ExternalReference(
                type=ExternalReferenceType.VCS,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python')
            ),
            ExternalReference(
                type=ExternalReferenceType.WEBSITE,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python/#readme')
            )
        ]))
    return bom
