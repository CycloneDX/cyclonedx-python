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
This module is internal - it is not public API.
All in here may have breaking change without notice.
"""

from typing import Optional

__LICENSE_TROVE_PREFIX = 'License :: '


def is_license_trove(classifier: str) -> bool:
    return classifier.startswith(__LICENSE_TROVE_PREFIX)


"""
Map of trove classifiers to SPDX license ID or SPDX license expression.

Some could be mapped to SPDX expressions, in case the version was not clear - like `(EFL-1.0 OR EFL-2.0)`.
! But this was not done yet, for uncertainties of [PEP639](https://peps.python.org/pep-0639)

classifiers: https://packaging.python.org/specifications/core-metadata/#metadata-classifier
- of list A: https://pypi.org/pypi?%3Aaction=list_classifiers
- of lList B: https://pypi.org/classifiers/

SPDX license IDs: https://spdx.org/licenses/

See also: https://peps.python.org/pep-0639/#mapping-license-classifiers-to-spdx-identifiers
"""
__TO_SPDX_MAP = {

    # region not  OSI Approved

    'License :: Aladdin Free Public License (AFPL)': 'Aladdin',
    'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication': 'CC0-1.0',
    'License :: CeCILL-B Free Software License Agreement (CECILL-B)': 'CECILL-B',
    'License :: CeCILL-C Free Software License Agreement (CECILL-C)': 'CECILL-C',
    # 'License :: Eiffel Forum License (EFL)': which one?
    #   -  EFL-1.0
    #   -  EFL-2.0
    # 'License :: Free For Educational Use': unknown to SPDX
    # 'License :: Free For Home Use': unknown to SPDX
    # 'License :: Free To Use But Restricted': unknown to SPDX
    # 'License :: Free for non-commercial use': unknown to SPDX
    # 'License :: Freely Distributable': unknown to SPDX
    # 'License :: Freeware': unknown to SPDX
    # 'License :: GUST Font License 1.0': unknown to SPDX,
    # 'License :: GUST Font License 2006-09-30': unknown to SPDX
    # 'License :: Netscape Public License (NPL)': which version?
    #   - NPL-1.0
    #   - NPL-1.1
    'License :: Nokia Open Source License (NOKOS)': 'Nokia',
    # 'License :: Other/Proprietary License': unknown to SPDX
    # 'License :: Public Domain': unknown to SPDX
    # 'License :: Repoze Public License': unknown to SPDX

    # endregion not  OSI Approved

    # region OSI Approved

    # !! reminder: the following are OSI approved, sp map only to the SPDX that ar marked as so
    # !! see the ideas and cases of https://peps.python.org/pep-0639/#mapping-license-classifiers-to-spdx-identifiers
    # 'License :: OSI Approved :: Academic Free License (AFL)': which one?
    #   -  AFL-1.1
    #   -  AFL-...
    #   -  AFL-3.0
    # 'License :: OSI Approved :: Apache Software License': which one?
    #    -  Apache-1.1
    #    -  Apache-2.0
    # 'License :: OSI Approved :: Apple Public Source License': which version?
    #    -  APSL-1.0
    #    -  APSL-2.0
    # 'License :: OSI Approved :: Artistic License': which version?
    #    - Artistic-1.0
    #    - Artistic-...
    #    - Artistic-3.0
    'License :: OSI Approved :: Attribution Assurance License': 'AAL',
    # 'License :: OSI Approved :: BSD License': which exactly?
    'License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)': 'BSL-1.0',
    'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)': 'CECILL-2.1',
    'License :: OSI Approved :: Common Development and Distribution License 1.0 (CDDL-1.0)': 'CDDL-1.0',
    'License :: OSI Approved :: Common Public License': 'CPL-1.0',
    'License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)': 'EPL-1.0',
    'License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)': 'EPL-1.0',
    # 'License :: OSI Approved :: Eiffel Forum License': which version?
    'License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)': 'EUPL-1.0',
    'License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)': 'EUPL-1.1',
    'License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)': 'EUPL-1.2',
    'License :: OSI Approved :: GNU Affero General Public License v3': 'AGPL-3.0-only',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)': 'AGPL-3.0-or-later',
    # 'License :: OSI Approved :: GNU Free Documentation License (FDL)': which version?
    # 'License :: OSI Approved :: GNU General Public License (GPL)': which version?
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)': 'GPL-2.0-only',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)': 'GPL-2.0-or-later',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)': 'GPL-3.0-only',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)': 'GPL-3.0-or-later',
    # 'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)': which one?
    #  - LGPL-2.0-only
    #  - LGPL-2.1-only
    # 'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)': which one?
    #  - LGPL-2.0-or-later
    #  - LGPL-2.1-or-later
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)': 'LGPL-3.0-only',
    'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)': 'LGPL-3.0-or-later',
    # 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)': which version?
    'License :: OSI Approved :: Historical Permission Notice and Disclaimer (HPND)': 'HPND',
    'License :: OSI Approved :: IBM Public License': 'IPL-1.0',
    'License :: OSI Approved :: ISC License (ISCL)': 'ISC',
    'License :: OSI Approved :: Intel Open Source License': 'Intel',
    # 'License :: OSI Approved :: Jabber Open Source License': unknown to SPDX
    'License :: OSI Approved :: MIT License': 'MIT',
    'License :: OSI Approved :: MIT No Attribution License (MIT-0)': 'MIT-0',
    # 'License :: OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)': unknown to SPDX
    'License :: OSI Approved :: MirOS License (MirOS)': 'MirOS',
    'License :: OSI Approved :: Motosoto License': 'Motosoto',
    'License :: OSI Approved :: Mozilla Public License 1.0 (MPL)': 'MPL-1.0',
    'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)': 'MPL-1.1',
    # 'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)': which one? MPL-XXX
    #   - MPL-2.0
    #   - MPL-2.0-no-copyleft-exception
    'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)': 'MulanPSL-1.0',
    'License :: OSI Approved :: Nethack General Public License': 'NGPL',
    'License :: OSI Approved :: Nokia Open Source License': 'Nokia',
    'License :: OSI Approved :: Open Group Test Suite License': 'OGTSL',
    'License :: OSI Approved :: Open Software License 3.0 (OSL-3.0)': 'OSL-3.0',
    'License :: OSI Approved :: PostgreSQL License': 'PostgreSQL',
    'License :: OSI Approved :: Python License (CNRI Python License)': 'CNRI-Python',
    'License :: OSI Approved :: Python Software Foundation License': 'Python-2.0',
    'License :: OSI Approved :: Qt Public License (QPL)': 'QPL-1.0',
    'License :: OSI Approved :: Ricoh Source Code Public License': 'RSCPL',
    # 'License :: OSI Approved :: SIL Open Font License 1.1 (OFL-1.1)': which one? OFL-XXX
    #   - OFL-1.1
    #   - OFL-1.1-no-RFN OFL-1.1-RFN
    'License :: OSI Approved :: Sleepycat License': 'Sleepycat',
    'License :: OSI Approved :: Sun Industry Standards Source License (SISSL)': 'SISSL',
    'License :: OSI Approved :: Sun Public License': 'SPL-1.0',
    'License :: OSI Approved :: The Unlicense (Unlicense)': 'Unlicense',
    'License :: OSI Approved :: Universal Permissive License (UPL)': 'UPL-1.0',
    'License :: OSI Approved :: University of Illinois/NCSA Open Source License': 'NCSA',
    'License :: OSI Approved :: Vovida Software License 1.0': 'VSL-1.0',
    'License :: OSI Approved :: W3C License': 'W3C',
    'License :: OSI Approved :: X.Net License': 'Xnet',
    # 'License :: OSI Approved :: Zope Public License': which one? ZPL-XXX
    #   - ZPL-2.0
    #   - ZPL-2.1
    'License :: OSI Approved :: zlib/libpng License': 'Zlib',

    # endregion OSI Approved
}


def license_trove2spdx(classifier: str) -> Optional[str]:
    """return the SPDX id or expression for a given license trove classifier"""
    return __TO_SPDX_MAP.get(classifier)
