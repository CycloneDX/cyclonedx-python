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
from typing import Dict, Optional, Any

from cyclonedx.exception.model import UnknownHashTypeException
from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType
from cyclonedx.model.component import Component
from cyclonedx.model.dependency import Dependency
from cyclonedx.parser import BaseParser
# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore
from toml import loads as load_toml


class PoetryParser(BaseParser):

    def __init__(self, poetry_lock_contents: str) -> None:
        super().__init__()
        poetry_lock = load_toml(poetry_lock_contents)

        for package in poetry_lock['package']:
            component = Component(
                name=package['name'], version=package['version'], purl=PackageURL(
                    type='pypi', name=package['name'], version=package['version']
                )
            )
            package_dependencies = package.get("dependencies")
            if package_dependencies is not None:
                for (name, _) in package_dependencies.items():
                    version = self._get_package_version_from_lock_dict(poetry_lock["package"], name)
                    d = Dependency(
                        purl=PackageURL(
                            type='pypi', name=name, version=version
                        )
                    )
                    component.add_dependency(d)

            for file_metadata in poetry_lock['metadata']['files'][package['name']]:
                try:
                    component.add_external_reference(ExternalReference(
                        reference_type=ExternalReferenceType.DISTRIBUTION,
                        url=component.get_pypi_url(),
                        comment=f'Distribution file: {file_metadata["file"]}',
                        hashes=[HashType.from_composite_str(file_metadata['hash'])]
                    ))
                except UnknownHashTypeException:
                    # @todo add logging for this type of exception?
                    pass

            self._components.append(component)

    def _get_package_version_from_lock_dict(self, poetry_lock_packages: Dict[Any, Any], name: str) -> Optional[str]:
        for package in poetry_lock_packages:
            if package["name"] == name:
                return str(package["version"])
        return None


class PoetryFileParser(PoetryParser):

    def __init__(self, poetry_lock_filename: str) -> None:
        with open(poetry_lock_filename) as r:
            super(PoetryFileParser, self).__init__(poetry_lock_contents=r.read())
        r.close()
