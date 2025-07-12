# This file is part of CycloneDX Python
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

from collections.abc import Iterable
from re import compile as re_compile
from typing import Any, Optional

from cyclonedx.builder.this import this_component as lib_component
from cyclonedx.model import ExternalReference, ExternalReferenceType, XsUri
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import (  # type:ignore[attr-defined]  # ComponentEvidence was moved, but is still importable - ignore/wont-fix for backwards compatibility  # noqa:E501
    Component,
    ComponentEvidence,
    ComponentType,
)
from cyclonedx.model.license import DisjunctiveLicense, License, LicenseAcknowledgement, LicenseExpression

from ... import __version__ as _THIS_VERSION  # noqa:N812


def make_bom(**kwargs: Any) -> Bom:
    bom = Bom(**kwargs)
    bom.metadata.tools.components.update((
        lib_component(),
        Component(
            type=ComponentType.APPLICATION,
            group='CycloneDX',
            # package is called 'cyclonedx-bom', but the tool is called 'cyclonedx-py'
            name='cyclonedx-py',
            version=_THIS_VERSION,
            description='CycloneDX Software Bill of Materials (SBOM) generator for Python projects and environments',
            licenses=(DisjunctiveLicense(id='Apache-2.0',
                                         acknowledgement=LicenseAcknowledgement.DECLARED),),
            external_references=(
                # let's assume this is not a fork
                ExternalReference(
                    type=ExternalReferenceType.WEBSITE,
                    url=XsUri('https://github.com/CycloneDX/cyclonedx-python/#readme')
                ),
                ExternalReference(
                    type=ExternalReferenceType.DOCUMENTATION,
                    url=XsUri('https://cyclonedx-bom-tool.readthedocs.io/')
                ),
                ExternalReference(
                    type=ExternalReferenceType.VCS,
                    url=XsUri('https://github.com/CycloneDX/cyclonedx-python/')
                ),
                ExternalReference(
                    type=ExternalReferenceType.BUILD_SYSTEM,
                    url=XsUri('https://github.com/CycloneDX/cyclonedx-python/actions')
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
                # we cannot assert where the lib was fetched from, but we can give a hint
                ExternalReference(
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri('https://pypi.org/project/cyclonedx-bom/')
                ),
            ),
            # to be extended...
        ),
    ))
    return bom


def find_LicenseExpression(licenses: Iterable['License']) -> Optional[LicenseExpression]:  # noqa: N802
    for license in licenses:
        if isinstance(license, LicenseExpression):
            return license
    return None


def licenses_fixup(component: 'Component') -> None:
    """
    Per CycloneDX spec, there must be EITHER one license expression OR multiple license id/name.
    If there is an expression, it is used and everything else is moved to evidences, so it is not lost.
    """
    # hack for preventing expressions AND named licenses.
    # see https://github.com/CycloneDX/cyclonedx-python/issues/826
    # see https://github.com/CycloneDX/specification/issues/454
    licenses = list(component.licenses)
    lexp = find_LicenseExpression(licenses)
    if lexp is None:
        return
    component.licenses = (lexp,)
    licenses.remove(lexp)
    if len(licenses) > 0:
        if component.evidence is None:
            component.evidence = ComponentEvidence()
        component.evidence.licenses.update(licenses)


_MAP_KNOWN_URL_LABELS: dict[str, ExternalReferenceType] = {
    # see https://peps.python.org/pep-0345/#project-url-multiple-use
    # see https://github.com/pypi/warehouse/issues/5947#issuecomment-699660629
    'bugtracker': ExternalReferenceType.ISSUE_TRACKER,
    'issuetracker': ExternalReferenceType.ISSUE_TRACKER,
    'issues': ExternalReferenceType.ISSUE_TRACKER,
    'bugreports': ExternalReferenceType.ISSUE_TRACKER,
    'tracker': ExternalReferenceType.ISSUE_TRACKER,
    'home': ExternalReferenceType.WEBSITE,
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

_NOCHAR_MATCHER = re_compile('[^a-z]')


def url_label_to_ert(value: str) -> ExternalReferenceType:
    return _MAP_KNOWN_URL_LABELS.get(
        _NOCHAR_MATCHER.sub('', str(value).lower()),
        ExternalReferenceType.OTHER
    )
