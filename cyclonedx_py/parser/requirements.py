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

import os
import os.path
from abc import ABCMeta
from tempfile import NamedTemporaryFile, _TemporaryFileWrapper  # Weak error
from typing import Any, Optional

from cyclonedx.model import HashType
from cyclonedx.model.component import Component
from cyclonedx.parser import BaseParser, ParserWarning

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore
from pip_requirements_parser import RequirementsFile  # type: ignore


class _BaseRequirementsParser(BaseParser, metaclass=ABCMeta):
    """Internal abstract parser - not for programmatic use.
    """

    def __init__(self, requirements_filename: str, include_nested: bool, use_purl_bom_ref: bool = False) -> None:
        super().__init__()
        parsed_rf: RequirementsFile = RequirementsFile.from_file(
            requirements_filename, include_nested=include_nested)

        for requirement in parsed_rf.requirements:
            name = requirement.link.url if requirement.is_local_path else requirement.name
            version = requirement.get_pinned_version or requirement.dumps_specifier()
            hashes = map(HashType.from_composite_str, requirement.hash_options)

            if not version and not requirement.is_local_path:
                self._warnings.append(
                    ParserWarning(
                        item=name,
                        warning=(f"Requirement \'{name}\' does not have a pinned "
                                 "version and cannot be included in your CycloneDX SBOM.")
                    )
                )
            else:
                purl = PackageURL(type='pypi', name=name, version=version)
                bom_ref = purl.to_string() if use_purl_bom_ref else None
                self._components.append(Component(
                    name=name,
                    bom_ref=bom_ref,
                    version=version,
                    hashes=hashes,
                    purl=purl
                ))


class RequirementsParser(_BaseRequirementsParser):

    def __init__(self, requirements_content: str, use_purl_bom_ref: bool = False) -> None:
        requirements_file: Optional[_TemporaryFileWrapper[Any]] = None

        requirements_file = NamedTemporaryFile(mode='w+', delete=False)
        try:
            requirements_file.write(requirements_content)
            requirements_file.close()
            super().__init__(
                requirements_filename=requirements_file.name,
                include_nested=False,
                use_purl_bom_ref=use_purl_bom_ref)
        finally:
            os.unlink(requirements_file.name)


class RequirementsFileParser(_BaseRequirementsParser):

    def __init__(self,
                 requirements_filename: str,
                 include_nested: bool = True,
                 use_purl_bom_ref: bool = False) -> None:
        super().__init__(
            requirements_filename=requirements_filename,
            include_nested=include_nested,
            use_purl_bom_ref=use_purl_bom_ref)
