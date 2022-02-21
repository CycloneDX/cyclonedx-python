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
from abc import ABCMeta, abstractmethod
from typing import List

from cyclonedx.model import ExternalReference, ExternalReferenceType, XsUri
from cyclonedx.model.component import Component
from cyclonedx.parser import BaseParser
# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore

from ..utils.conda import parse_conda_json_to_conda_package, parse_conda_list_str_to_conda_package, CondaPackage


class _BaseCondaParser(BaseParser, metaclass=ABCMeta):
    """Internal abstract parser - not for programmatic use.
    """

    def __init__(self, conda_data: str) -> None:
        super().__init__()
        self._conda_packages: List[CondaPackage] = []
        self._parse_to_conda_packages(data_str=conda_data)
        self._conda_packages_to_components()

    @abstractmethod
    def _parse_to_conda_packages(self, data_str: str) -> None:
        """
        Abstract method for implementation by concrete Conda Parsers.

        Implementation should add a `list` of `CondaPackage` instances to `self._conda_packages`

        Params:
            data_str:
                `str` data passed into the Parser
        """
        pass

    def _conda_packages_to_components(self) -> None:
        """
        Converts the parsed `CondaPackage` instances into `Component` instances.

        """
        for conda_package in self._conda_packages:
            c = Component(
                name=conda_package['name'], version=str(conda_package['version']),
                purl=PackageURL(
                    type='pypi', name=conda_package['name'], version=str(conda_package['version'])
                )
            )
            c.external_references.add(ExternalReference(
                reference_type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(conda_package['base_url']),
                comment=f"Distribution name {conda_package['dist_name']}"
            ))

            self._components.append(c)


class CondaListJsonParser(_BaseCondaParser):
    """
    This parser is intended to receive the output from the command `conda list --json`.
    """

    def _parse_to_conda_packages(self, data_str: str) -> None:
        conda_list_content = json.loads(data_str)

        for package in conda_list_content:
            conda_package = parse_conda_json_to_conda_package(conda_json_str=json.dumps(package))
            if conda_package:
                self._conda_packages.append(conda_package)


class CondaListExplicitParser(_BaseCondaParser):
    """
    This parser is intended to receive the output from the command `conda list --explicit` or
    `conda list --explicit --md5`.
    """

    def _parse_to_conda_packages(self, data_str: str) -> None:
        for line in data_str.replace('\r\n', '\n').split('\n'):
            line = line.strip()
            conda_package = parse_conda_list_str_to_conda_package(conda_list_str=line)
            if conda_package:
                self._conda_packages.append(conda_package)
