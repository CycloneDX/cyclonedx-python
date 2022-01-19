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

from packageurl import PackageURL

from cyclonedx_py.parser.poetry import PoetryFileParser


class TestPoetryParser(TestCase):

    def test_simple(self) -> None:
        tests_poetry_lock_file = os.path.join(os.path.dirname(__file__), 'fixtures/poetry-lock-simple.txt')

        parser = PoetryFileParser(poetry_lock_filename=tests_poetry_lock_file)
        self.assertEqual(2, parser.component_count())
        components = parser.get_components()
        self.assertEqual('pluggy', components[0].name)
        self.assertEqual('1.0.0', components[0].version)
        self.assertEqual('importlib-metadata', components[1].name)
        self.assertEqual('4.8.1', components[1].version)
        self.assertEqual(len(components[0].external_references), 2)
        dependencies = components[0].get_dependencies()
        self.assertEqual(1, len(dependencies))
        self.assertEqual(PackageURL(type="pypi", name="importlib-metadata", version="4.8.1"), dependencies[0].purl)
