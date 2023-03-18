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
from unittest import TestCase

from ddt import data, ddt

from cyclonedx_py.parser.poetry import OmitCategory, PoetryFileParser


@ddt
class TestPoetryParser(TestCase):

    @data('poetry-lock11-simple.txt',
          'poetry-lock20-simple.txt')
    def test_simple(self, lock_file_name: str) -> None:
        poetry_lock_filename = os.path.join(os.path.dirname(__file__), 'fixtures', lock_file_name)
        parser = PoetryFileParser(
            poetry_lock_filename=poetry_lock_filename,
            omit_category=set())
        self.assertEqual(1, parser.component_count())
        component = next(filter(lambda c: c.name == 'toml', parser.get_components()), None)
        self.assertIsNotNone(component)
        self.assertEqual('toml', component.name)
        self.assertNotEqual(component.purl.to_string(), component.bom_ref.value)
        self.assertEqual('0.10.2', component.version)
        self.assertEqual(2, len(component.external_references), f'{component.external_references}')

    @data('poetry-lock11-simple.txt',
          'poetry-lock20-simple.txt')
    def test_simple_purl_bom_ref(self, lock_file_name: str) -> None:
        poetry_lock_filename = os.path.join(os.path.dirname(__file__), 'fixtures', lock_file_name)
        parser = PoetryFileParser(
            poetry_lock_filename=poetry_lock_filename,
            omit_category=set(),
            use_purl_bom_ref=True)
        self.assertEqual(1, parser.component_count())
        component = next(filter(lambda c: c.name == 'toml', parser.get_components()), None)
        self.assertIsNotNone(component)
        self.assertEqual('toml', component.name)
        self.assertEqual(component.purl.to_string(), component.bom_ref.value)
        self.assertEqual('0.10.2', component.version)
        self.assertEqual(2, len(component.external_references), f'{component.external_references}')

    @data('poetry-dev-dep.txt')
    def test_ignore_dev_dep(self, lock_file_name: str) -> None:
        poetry_lock_filename = os.path.join(os.path.dirname(__file__), 'fixtures', lock_file_name)

        # without omit
        parser = PoetryFileParser(
            poetry_lock_filename=poetry_lock_filename,
            omit_category=set(),
            use_purl_bom_ref=True)
        self.assertEqual(2, parser.component_count())
        component = next(filter(lambda c: c.name == 'toml', parser.get_components()), None)
        self.assertIsNotNone(component)
        self.assertEqual('toml', component.name)
        self.assertEqual(component.purl.to_string(), component.bom_ref.value)
        self.assertEqual('0.10.2', component.version)
        self.assertEqual(2, len(component.external_references), f'{component.external_references}')
        self.assertEqual(1, len(component.properties))
        prop = next(iter(component.properties))
        self.assertEqual('cdx:poetry:package:group', prop.name)
        self.assertEqual('main', prop.value)

        component = next(filter(lambda c: c.name == 'ddt', parser.get_components()), None)
        self.assertIsNotNone(component)
        self.assertEqual('ddt', component.name)
        self.assertEqual(component.purl.to_string(), component.bom_ref.value)
        self.assertEqual('1.6.0', component.version)
        self.assertEqual(2, len(component.external_references), f'{component.external_references}')
        self.assertEqual(1, len(component.properties))
        prop = next(iter(component.properties))
        self.assertEqual('cdx:poetry:package:group', prop.name)
        self.assertEqual('dev', prop.value)

        # with omit
        parser = PoetryFileParser(
            poetry_lock_filename=poetry_lock_filename,
            omit_category={OmitCategory.DEV},
            use_purl_bom_ref=True)
        self.assertEqual(1, parser.component_count())
        component = next(filter(lambda c: c.name == 'toml', parser.get_components()), None)
        self.assertIsNotNone(component)
        self.assertEqual('toml', component.name)
        self.assertEqual(component.purl.to_string(), component.bom_ref.value)
        self.assertEqual('0.10.2', component.version)
        self.assertEqual(2, len(component.external_references), f'{component.external_references}')
        self.assertEqual(1, len(component.properties))
        prop = next(iter(component.properties))
        self.assertEqual('cdx:poetry:package:group', prop.name)
        self.assertEqual('main', prop.value)
