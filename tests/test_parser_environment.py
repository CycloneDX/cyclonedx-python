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
import sys
from unittest import TestCase

from cyclonedx.model import License, LicenseChoice

from cyclonedx_py.parser.environment import EnvironmentParser


class TestEnvironmentParser(TestCase):

    def test_simple(self) -> None:
        """
        @todo This test is a vague as it will detect the unique environment where tests are being executed -
                so is this valid?

        :return:
        """
        parser = EnvironmentParser()
        self.assertGreater(parser.component_count(), 1)

        # We can only be sure that tox is in the environment, for example as we use tox to run tests
        c_tox = next(filter(lambda c: c.name == 'tox', parser.get_components()), None)
        self.assertIsNotNone(c_tox)
        self.assertNotEqual(c_tox.purl.to_string(), c_tox.bom_ref.value)
        self.assertIsNotNone(c_tox.licenses)
        self.assertEqual(len(c_tox.licenses), 2)
        self.assertEqual({LicenseChoice(license_=License(license_name="MIT License")),
                          LicenseChoice(license_=License(license_name="MIT"))}, c_tox.licenses)

    def test_simple_use_purl_bom_ref(self) -> None:
        """
        @todo This test is a vague as it will detect the unique environment where tests are being executed -
                so is this valid?

        :return:
        """
        parser = EnvironmentParser(use_purl_bom_ref=True)
        self.assertGreater(parser.component_count(), 1)

        # We can only be sure that tox is in the environment, for example as we use tox to run tests
        c_tox = next(filter(lambda c: c.name == 'tox', parser.get_components()), None)
        self.assertIsNotNone(c_tox)
        self.assertEqual(c_tox.purl.to_string(), c_tox.bom_ref.value)
        self.assertIsNotNone(c_tox.licenses)
        self.assertEqual(len(c_tox.licenses), 2)
        self.assertEqual({LicenseChoice(license_=License(license_name="MIT License")),
                          LicenseChoice(license_=License(license_name="MIT"))}, c_tox.licenses)

    def test_simple_use_location_filter(self) -> None:
        # Ensure that it makes no difference if we pass the complete sys.path
        # as location filter or no filter at all
        parser_sys_path = EnvironmentParser(location_filter=sys.path)
        self.assertGreater(parser_sys_path.component_count(), 1)

        parser_no_filter = EnvironmentParser()
        self.assertGreater(parser_no_filter.component_count(), 1)
        self.assertEqual(parser_no_filter.component_count(), parser_sys_path.component_count())

        # ensure that no components are found if we set the location filter
        # to a non existing path
        parser_invalid_filter = EnvironmentParser(location_filter=["/tmp/fa12b66cac07e4bb480e98eba9627737"])
        self.assertEqual(parser_invalid_filter.component_count(), 0)

    def test_simple_use_requiremets(self) -> None:
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/requirements-simple.txt')) as r:
            parser = EnvironmentParser(requirements_content=r.read())
        components = parser.get_components()
        self.assertEqual(1, len(components))

        parser = EnvironmentParser(requirements_content=os.path.join(os.path.dirname(__file__),
                                                                     'fixtures/requirements-simple.txt'))
        components = parser.get_components()
        self.assertGreaterEqual(1, len(components), f"{components}")

        parser = EnvironmentParser(
            location_filter=["/tmp/fa12b66cac07e4bb480e98eba9627737"],
            requirements_content=os.path.join(os.path.dirname(__file__),
                                              'fixtures/requirements-simple.txt'))
        components = parser.get_components()
        self.assertGreaterEqual(0, len(components))
