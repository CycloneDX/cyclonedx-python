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
Pure mapping data for URL -> ExternalReferenceType classification.

This module is DATA ONLY -- no logic. To extend classification, add rows here.
Four match styles, applied by ``cdx.url_label_to_ert`` in this precedence order:

1. _MAP_KNOWN_URL_LABELS        exact label (normalized: lowercased, non-[a-z] stripped)
2. _MAP_URL_LABEL_PREFIXES      label prefix (PyPI '*' semantics); first match wins
3. _MAP_KNOWN_URL_HOST_SUFFIXES host == key OR host endswith '.'+key (domain + subdomains)
4. _MAP_KNOWN_URL_HOST_PREFIXES host == key OR host startswith key+'.' (e.g. docs.*)

Label keys MUST already be normalized (lowercase, only [a-z]).
Host keys MUST be lowercase.

see https://docs.pypi.org/project_metadata/#icons
"""

from cyclonedx.model import ExternalReferenceType

# 1. exact label -> ERT
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
    'releasenotes': ExternalReferenceType.RELEASE_NOTES,
    'news': ExternalReferenceType.RELEASE_NOTES,
    'whatsnew': ExternalReferenceType.RELEASE_NOTES,
    'history': ExternalReferenceType.RELEASE_NOTES,
    'repository': ExternalReferenceType.VCS,
    'source': ExternalReferenceType.VCS,
    'github': ExternalReferenceType.VCS,
    'chat': ExternalReferenceType.CHAT,
}

# 2. label prefix -> ERT (ordered; first match wins). normalized prefixes.
_MAP_URL_LABEL_PREFIXES: tuple[tuple[str, ExternalReferenceType], ...] = (
    ('documentation', ExternalReferenceType.DOCUMENTATION),
    ('docs', ExternalReferenceType.DOCUMENTATION),
    ('bug', ExternalReferenceType.ISSUE_TRACKER),
    ('issue', ExternalReferenceType.ISSUE_TRACKER),
    ('tracker', ExternalReferenceType.ISSUE_TRACKER),
    ('report', ExternalReferenceType.ISSUE_TRACKER),
    ('funding', ExternalReferenceType.OTHER),
    ('sponsor', ExternalReferenceType.OTHER),
    ('donation', ExternalReferenceType.OTHER),
    ('donate', ExternalReferenceType.OTHER),
)
