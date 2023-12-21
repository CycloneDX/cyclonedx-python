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


"""
CycloneDX related helpers and utils.
"""

from re import compile as re_compile
from typing import Any, Dict, Iterable, Optional

from cyclonedx.model import ExternalReference, ExternalReferenceType, Tool, XsUri, HashAlgorithm
from cyclonedx.model.bom import Bom
from cyclonedx.model.license import License, LicenseExpression

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


def licenses_fixup(licenses: Iterable['License']) -> Iterable['License']:
    licenses = set(licenses)
    for license in licenses:
        if isinstance(license, LicenseExpression):
            return (license,)
    return licenses


__known_ulr_labels: Dict[str, ExternalReferenceType] = {
    # see https://peps.python.org/pep-0345/#project-url-multiple-use
    # see https://github.com/pypi/warehouse/issues/5947#issuecomment-699660629
    'bugtracker': ExternalReferenceType.ISSUE_TRACKER,
    'issuetracker': ExternalReferenceType.ISSUE_TRACKER,
    'issues': ExternalReferenceType.ISSUE_TRACKER,
    'bugreports': ExternalReferenceType.ISSUE_TRACKER,
    'tracker': ExternalReferenceType.ISSUE_TRACKER,
    'homepage': ExternalReferenceType.WEBSITE,
    'download': ExternalReferenceType.DISTRIBUTION,
    'documentation': ExternalReferenceType.DOCUMENTATION,
    'docs': ExternalReferenceType.DOCUMENTATION,
    'changelog': ExternalReferenceType.RELEASE_NOTES,
    'changes': ExternalReferenceType.RELEASE_NOTES,
    # 'source': ExternalReferenceType.SOURCE-DISTRIBUTION,
    'repository': ExternalReferenceType.VCS,
    'github': ExternalReferenceType.VCS,
    'chat': ExternalReferenceType.CHAT,
}

__re_nochar = re_compile('[^a-z]')


def url_label_to_ert(value: str) -> ExternalReferenceType:
    return __known_ulr_labels.get(
        __re_nochar.sub('', str(value).lower()),
        ExternalReferenceType.OTHER)


__map_hashlib: Dict[str, HashAlgorithm] = {
    # from hashlib.algorithms_guaranteed
    # TODO move to py-lib
    'md5': HashAlgorithm.MD5,
    'sha1': HashAlgorithm.SHA_1,
    'sha256': HashAlgorithm.SHA_256,
    'sha384': HashAlgorithm.SHA_384,
    'sha512': HashAlgorithm.SHA_512,
    'sha3_384': HashAlgorithm.SHA3_384,
    'sha3_256': HashAlgorithm.SHA3_256,
    'sha3_512': HashAlgorithm.SHA3_512,
}


def hashlib_alg_to_ha(alg: str) -> Optional[HashAlgorithm]:
    return __map_hashlib.get(alg)
