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

from cyclonedx.exception.model import CycloneDxModelException
from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, XsUri
from cyclonedx.model.component import Component
from cyclonedx.parser import BaseParser

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore
from toml import loads as load_toml

from ._debug import DebugMessageCallback, quiet


class PoetryParser(BaseParser):

    def __init__(
            self, poetry_lock_contents: str, use_purl_bom_ref: bool = False,
            *,
            debug_message: DebugMessageCallback = quiet
    ) -> None:
        super().__init__()
        debug_message('init {}', self.__class__.__name__)

        debug_message('loading poetry_lock_contents')
        poetry_lock = load_toml(poetry_lock_contents)

        poetry_lock_metadata = poetry_lock['metadata']
        try:
            poetry_lock_version = tuple(int(p) for p in str(poetry_lock_metadata['lock-version']).split('.'))
        except Exception:
            poetry_lock_version = (0,)
        debug_message('detected poetry_lock_version: {!r}', poetry_lock_version)

        debug_message('processing poetry_lock')
        for package in poetry_lock['package']:
            debug_message('processing package: {!r}', package)
            purl = PackageURL(type='pypi', name=package['name'], version=package['version'])
            bom_ref = purl.to_string() if use_purl_bom_ref else None
            component = Component(
                name=package['name'], bom_ref=bom_ref, version=package['version'],
                purl=purl
            )
            debug_message('detecting package_files')
            package_files = package['files'] \
                if poetry_lock_version >= (2,) \
                else poetry_lock_metadata['files'][package['name']]
            debug_message('processing package_files: {!r}', package_files)
            for file_metadata in package_files:
                debug_message('processing file_metadata: {!r}', file_metadata)
                try:
                    component.external_references.add(ExternalReference(
                        reference_type=ExternalReferenceType.DISTRIBUTION,
                        url=XsUri(component.get_pypi_url()),
                        comment=f'Distribution file: {file_metadata["file"]}',
                        hashes=[HashType.from_composite_str(file_metadata['hash'])]
                    ))
                except CycloneDxModelException as error:
                    # @todo traceback and details to the output?
                    debug_message('Warning: suppressed {!r}', error)
                    del error
            self._components.append(component)


class PoetryFileParser(PoetryParser):

    def __init__(
            self, poetry_lock_filename: str, use_purl_bom_ref: bool = False,
            *,
            debug_message: DebugMessageCallback = quiet
    ) -> None:
        debug_message('open file: {}', poetry_lock_filename)
        with open(poetry_lock_filename) as plf:
            super(PoetryFileParser, self).__init__(
                poetry_lock_contents=plf.read(), use_purl_bom_ref=use_purl_bom_ref,
                debug_message=debug_message
            )
