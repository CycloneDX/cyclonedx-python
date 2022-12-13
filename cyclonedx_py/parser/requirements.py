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
from tempfile import NamedTemporaryFile  # Weak error

from cyclonedx.model import HashType
from cyclonedx.model.component import Component
from cyclonedx.parser import BaseParser, ParserWarning

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore
from pip_requirements_parser import RequirementsFile  # type: ignore

from ._debug import DebugMessageCallback, quiet


class RequirementsParser(BaseParser):

    def __init__(
            self, requirements_content: str, use_purl_bom_ref: bool = False,
            *,
            debug_message: DebugMessageCallback = quiet
    ) -> None:
        super().__init__()
        debug_message('init {}', self.__class__.__name__)

        if os.path.exists(requirements_content):
            debug_message('create RequirementsFile from file: {}', requirements_content)
            parsed_rf = RequirementsFile.from_file(requirements_content, include_nested=True)
        else:
            with NamedTemporaryFile(mode='w+', delete=False) as requirements_file:
                debug_message('write requirements_content to TempFile: {}', requirements_file.name)
                requirements_file.write(requirements_content)
            try:
                debug_message('create RequirementsFile from TempFile: {}', requirements_file.name)
                parsed_rf = RequirementsFile.from_file(requirements_file.name, include_nested=False)
            finally:
                debug_message('unlink TempFile: {}', requirements_file.name)
                os.unlink(requirements_file.name)
            del requirements_file

        debug_message('processing requirements')
        for requirement in parsed_rf.requirements:
            debug_message('processing requirement: {!r}', requirement)
            name = requirement.link.url if requirement.is_local_path else requirement.name
            version = requirement.get_pinned_version or requirement.dumps_specifier()
            debug_message('detected: {!r} {!r}', name, version)
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


class RequirementsFileParser(RequirementsParser):

    def __init__(
            self, requirements_file: str, use_purl_bom_ref: bool = False,
            *,
            debug_message: DebugMessageCallback = quiet
    ) -> None:
        super().__init__(
            requirements_content=requirements_file, use_purl_bom_ref=use_purl_bom_ref,
            debug_message=debug_message
        )
