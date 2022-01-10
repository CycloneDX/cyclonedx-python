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

from cyclonedx.parser.pipenv import PipEnvFileParser


class TestPipEnvParser(TestCase):

    def test_simple(self) -> None:
        tests_pipfile_lock = os.path.join(os.path.dirname(__file__), 'fixtures/pipfile-lock-simple.txt')

        parser = PipEnvFileParser(pipenv_lock_filename=tests_pipfile_lock)
        self.assertEqual(1, parser.component_count())
        components = parser.get_components()

        self.assertEqual('toml', components[0].name)
        self.assertEqual('0.10.2', components[0].version)
        self.assertEqual(len(components[0].external_references), 2)
        self.assertEqual(len(components[0].external_references[0].get_hashes()), 1)

    def test_with_multiple_and_no_index(self) -> None:
        tests_pipfile_lock = os.path.join(os.path.dirname(__file__), 'fixtures/pipfile-lock-no-index-example.txt')

        parser = PipEnvFileParser(pipenv_lock_filename=tests_pipfile_lock)
        self.assertEqual(2, parser.component_count())
        components = parser.get_components()

        c_anyio = [x for x in components if x.name == 'anyio'][0]
        c_toml = [x for x in components if x.name == 'toml'][0]

        self.assertEqual('anyio', c_anyio.name)
        self.assertEqual('3.3.3', c_anyio.version)
        self.assertEqual(0, len(c_anyio.external_references))

        self.assertEqual('toml', c_toml.name)
        self.assertEqual('0.10.2', c_toml.version)
        self.assertEqual(len(c_toml.external_references), 2)
        self.assertEqual(len(c_toml.external_references[0].get_hashes()), 1)
