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

from cyclonedx.parser.conda import CondaListJsonParser, CondaListExplicitParser


class TestCondaParser(TestCase):

    def test_conda_list_json(self) -> None:
        conda_list_ouptut_file = os.path.join(os.path.dirname(__file__), 'fixtures/conda-list-output.json')

        with (open(conda_list_ouptut_file, 'r')) as conda_list_ouptut_fh:
            parser = CondaListJsonParser(conda_data=conda_list_ouptut_fh.read())
            conda_list_ouptut_fh.close()

        self.assertEqual(34, parser.component_count())
        components = parser.get_components()

        c_noarch = [x for x in components if x.name == 'idna'][0]
        self.assertEqual('idna', c_noarch.name)
        self.assertEqual('2.10', c_noarch.version)
        self.assertEqual(1, len(c_noarch.external_references))
        self.assertEqual(0, len(c_noarch.external_references[0].get_hashes()))

    def test_conda_list_explicit_md5(self) -> None:
        conda_list_ouptut_file = os.path.join(os.path.dirname(__file__), 'fixtures/conda-list-explicit-md5.txt')

        with (open(conda_list_ouptut_file, 'r')) as conda_list_ouptut_fh:
            parser = CondaListExplicitParser(conda_data=conda_list_ouptut_fh.read())
            conda_list_ouptut_fh.close()

        self.assertEqual(34, parser.component_count())
        components = parser.get_components()

        c_noarch = [x for x in components if x.name == 'idna'][0]
        self.assertEqual('idna', c_noarch.name)
        self.assertEqual('2.10', c_noarch.version)
        self.assertEqual(1, len(c_noarch.external_references))
        self.assertEqual(0, len(c_noarch.external_references[0].get_hashes()))
