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

from cyclonedx.model.component import Component
from cyclonedx.parser import BaseParser, ParserWarning
# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore
from pkg_resources import parse_requirements as parse_requirements


class RequirementsParser(BaseParser):

    def __init__(self, requirements_content: str) -> None:
        super().__init__()

        requirements = parse_requirements(requirements_content)
        for requirement in requirements:
            """
            @todo
            Note that the below line will get the first (lowest) version specified in the Requirement and
            ignore the operator (it might not be ==). This is passed to the Component.

            For example if a requirement was listed as: "PickyThing>1.6,<=1.9,!=1.8.6", we'll be interpreting this
            as if it were written "PickyThing==1.6"
            """
            try:
                (op, version) = requirement.specs[0]
                self._components.append(Component(
                    name=requirement.project_name, version=version, purl=PackageURL(
                        type='pypi', name=requirement.project_name, version=version
                    )
                ))
            except IndexError:
                self._warnings.append(
                    ParserWarning(
                        item=requirement.project_name,
                        warning='Requirement \'{}\' does not have a pinned version and cannot be included in your '
                                'CycloneDX SBOM.'.format(requirement.project_name)
                    )
                )


class RequirementsFileParser(RequirementsParser):

    def __init__(self, requirements_file: str) -> None:
        with open(requirements_file) as r:
            super(RequirementsFileParser, self).__init__(requirements_content=r.read())
            r.close()
