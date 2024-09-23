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


from typing import Any, Dict, Iterable, Tuple, Union
from unittest import TestCase

from cyclonedx.model import ExternalReference, ExternalReferenceType
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.license import License, LicenseAcknowledgement

from cyclonedx_py._internal.utils.cdx import make_bom
from tests import EXPECTED_TOOL_NAME, load_pyproject


class ExtRefsTestMixin:

    @staticmethod
    def __first_ers_uri(t: ExternalReferenceType, ers: Iterable[ExternalReference]) -> str:
        return next(filter(lambda r: r.type is t, ers)).url.uri

    def assertExtRefs(  # noqa:N802
        self: Union[TestCase, 'ExtRefsTestMixin'],
        p: Dict[str, Any], ers: Iterable[ExternalReference]
    ) -> None:
        self.assertEqual(p['tool']['poetry']['homepage'], self.__first_ers_uri(
            ExternalReferenceType.WEBSITE, ers))
        self.assertEqual(p['tool']['poetry']['repository'], self.__first_ers_uri(
            ExternalReferenceType.VCS, ers))
        self.assertEqual(p['tool']['poetry']['documentation'], self.__first_ers_uri(
            ExternalReferenceType.DOCUMENTATION, ers))
        self.assertEqual(p['tool']['poetry']['urls']['Bug Tracker'], self.__first_ers_uri(
            ExternalReferenceType.ISSUE_TRACKER, ers))


class TestThisComponentInMetadataTools(TestCase, ExtRefsTestMixin):
    def __get_c_by_name(self, n: str) -> Component:
        c = next(filter(lambda o: o.name == n,
                        make_bom().metadata.tools.components))
        self.assertIsNotNone(c)
        return c

    def test_basics(self) -> None:
        p = load_pyproject()
        c = self.__get_c_by_name(EXPECTED_TOOL_NAME)
        self.assertIs(ComponentType.APPLICATION, c.type)
        self.assertEqual('CycloneDX', c.group)
        self.assertEqual(EXPECTED_TOOL_NAME, c.name)
        self.assertEqual(p['tool']['poetry']['version'], c.version)
        self.assertEqual(p['tool']['poetry']['description'], c.description)

    def test_license(self) -> None:
        p = load_pyproject()
        c = self.__get_c_by_name(EXPECTED_TOOL_NAME)
        ls: Tuple[License, ...] = tuple(c.licenses)
        self.assertEqual(1, len(ls))
        l = ls[0]  # noqa:E741
        self.assertIs(LicenseAcknowledgement.DECLARED, l.acknowledgement)
        # this uses the fact that poetry expect license declarations as valid SPDX-license-id
        self.assertEqual(p['tool']['poetry']['license'], l.id)

    def test_extrefs(self) -> None:
        p = load_pyproject()
        c = self.__get_c_by_name(EXPECTED_TOOL_NAME)
        ers: Tuple[ExternalReference, ...] = tuple(c.external_references)
        self.assertExtRefs(p, ers)
