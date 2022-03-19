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

from cyclonedx_py.parser.conda import CondaListExplicitParser, CondaListJsonParser


class TestCondaParser(TestCase):

    def test_conda_list_json(self) -> None:
        conda_list_ouptut_file = os.path.join(os.path.dirname(__file__), 'fixtures/conda-list-output.json')

        with (open(conda_list_ouptut_file, 'r')) as conda_list_output_fh:
            parser = CondaListJsonParser(conda_data=conda_list_output_fh.read())

        self.assertEqual(34, parser.component_count())
        components = parser.get_components()

        c_idna = next(filter(lambda c: c.name == 'idna', components), None)
        self.assertIsNotNone(c_idna)
        self.assertEqual('idna', c_idna.name)
        self.assertEqual('2.10', c_idna.version)
        self.assertEqual(1, len(c_idna.external_references), f'{c_idna.external_references}')
        self.assertEqual(0, len(c_idna.external_references.pop().hashes))

    def test_conda_list_explicit_md5(self) -> None:
        conda_list_ouptut_file = os.path.join(os.path.dirname(__file__), 'fixtures/conda-list-explicit-md5.txt')

        with (open(conda_list_ouptut_file, 'r')) as conda_list_output_fh:
            parser = CondaListExplicitParser(conda_data=conda_list_output_fh.read())

        self.assertEqual(34, parser.component_count())
        components = parser.get_components()

        c_idna = next(filter(lambda c: c.name == 'idna', components), None)
        self.assertIsNotNone(c_idna)
        self.assertEqual('idna', c_idna.name)
        self.assertEqual('2.10', c_idna.version)
        self.assertEqual(1, len(c_idna.external_references), f'{c_idna.external_references}')
        self.assertEqual(0, len(c_idna.external_references.pop().hashes))
