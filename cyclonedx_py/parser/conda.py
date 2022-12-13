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

from cyclonedx.model import ExternalReference, ExternalReferenceType, HashAlgorithm, HashType, XsUri
from cyclonedx.model.component import Component
from cyclonedx.parser import BaseParser

from ..utils.conda import (
    CondaPackage,
    conda_package_to_purl,
    parse_conda_json_to_conda_package,
    parse_conda_list_str_to_conda_package,
)
from ._debug import DebugMessageCallback, quiet


class _BaseCondaParser(BaseParser, metaclass=ABCMeta):
    """Internal abstract parser - not for programmatic use.
    """

    def __init__(
            self, conda_data: str, use_purl_bom_ref: bool = False,
            *,
            debug_message: DebugMessageCallback = quiet
    ) -> None:
        super().__init__()
        debug_message('init {}', self.__class__.__name__)
        self._debug_message = debug_message
        self._conda_packages: List[CondaPackage] = []
        self._parse_to_conda_packages(data_str=conda_data)
        self._conda_packages_to_components(use_purl_bom_ref=use_purl_bom_ref)

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

    def _conda_packages_to_components(self, use_purl_bom_ref: bool) -> None:
        """
        Converts the parsed `CondaPackage` instances into `Component` instances.

        """
        self._debug_message('processing conda_packages')
        for conda_package in self._conda_packages:
            self._debug_message('processing conda_package: {!r}', conda_package)
            purl = conda_package_to_purl(conda_package)
            bom_ref = purl.to_string() if use_purl_bom_ref else None
            c = Component(
                name=conda_package['name'], bom_ref=bom_ref, version=conda_package['version'],
                purl=purl
            )
            c.external_references.add(ExternalReference(
                reference_type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri(conda_package['base_url']),
                comment=f"Distribution name {conda_package['dist_name']}"
            ))
            if conda_package['md5_hash'] is not None:
                c.hashes.add(HashType(
                    algorithm=HashAlgorithm.MD5,
                    hash_value=str(conda_package['md5_hash'])
                ))

            self._components.append(c)


class CondaListJsonParser(_BaseCondaParser):
    """
    This parser is intended to receive the output from the command `conda list --json`.
    """

    def _parse_to_conda_packages(self, data_str: str) -> None:
        conda_list_content = json.loads(data_str)
        self._debug_message('processing conda_list_content')
        for package in conda_list_content:
            self._debug_message('processing package: {!r}', package)
            conda_package = parse_conda_json_to_conda_package(conda_json_str=json.dumps(package))
            if conda_package:
                self._conda_packages.append(conda_package)
            else:
                self._debug_message('no conda_package -> skip')


class CondaListExplicitParser(_BaseCondaParser):
    """
    This parser is intended to receive the output from the command `conda list --explicit` or
    `conda list --explicit --md5`.
    """

    def _parse_to_conda_packages(self, data_str: str) -> None:
        self._debug_message('processing data_str')
        for line in data_str.replace('\r\n', '\n').split('\n'):
            line = line.strip()
            self._debug_message('processing line: {}', line)
            conda_package = parse_conda_list_str_to_conda_package(conda_list_str=line)
            if conda_package:
                self._conda_packages.append(conda_package)
            else:
                self._debug_message('no conda_package -> skip')
