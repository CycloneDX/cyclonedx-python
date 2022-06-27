# encoding: utf-8

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

import json
from typing import Any, Dict

from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, XsUri
from cyclonedx.model.component import Component
from cyclonedx.parser import BaseParser

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore


class PipEnvParser(BaseParser):

    def __init__(self, pipenv_contents: str, use_purl_bom_ref: bool = False) -> None:
        super().__init__()

        pipfile_lock_contents = json.loads(pipenv_contents)
        pipfile_default: Dict[str, Dict[str, Any]] = pipfile_lock_contents.get('default') or {}

        for (package_name, package_data) in pipfile_default.items():
            version = str(package_data.get('version') or 'unknown').lstrip('=')
            purl = PackageURL(type='pypi', name=package_name, version=version)
            bom_ref = purl.to_string() if use_purl_bom_ref else None
            c = Component(name=package_name, bom_ref=bom_ref, version=version, purl=purl)
            if isinstance(package_data.get('hashes'), list):
                # Add download location with hashes stored in Pipfile.lock
                for pip_hash in package_data['hashes']:
                    ext_ref = ExternalReference(
                        reference_type=ExternalReferenceType.DISTRIBUTION,
                        url=XsUri(c.get_pypi_url()),
                        comment='Distribution available from pypi.org'
                    )
                    ext_ref.hashes.add(HashType.from_composite_str(pip_hash))
                    c.external_references.add(ext_ref)

            self._components.append(c)


class PipEnvFileParser(PipEnvParser):

    def __init__(self, pipenv_lock_filename: str, use_purl_bom_ref: bool = False) -> None:
        with open(pipenv_lock_filename) as r:
            super(PipEnvFileParser, self).__init__(pipenv_contents=r.read(), use_purl_bom_ref=use_purl_bom_ref)
