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
import re
from unittest import TestCase

from cyclonedx.model import HashAlgorithm, HashType

from cyclonedx_py.parser.conda import CondaListExplicitParser, CondaListJsonParser


class TestCondaParser(TestCase):

    def test_conda_list_json(self) -> None:
        conda_list_output_file = os.path.join(os.path.dirname(__file__),
                                              'fixtures/conda-list-output.json')

        with (open(conda_list_output_file, 'r')) as conda_list_output_fh:
            parser = CondaListJsonParser(conda_data=conda_list_output_fh.read())

        self.assertEqual(34, parser.component_count())
        components = parser.get_components()

        c_idna = next(filter(lambda c: c.name == 'idna', components), None)
        self.assertIsNotNone(c_idna)
        self.assertEqual('idna', c_idna.name)
        self.assertNotEqual(c_idna.purl.to_string(), c_idna.bom_ref.value)
        self.assertEqual('2.10', c_idna.version)
        self.assertEqual('pkg:conda/idna@2.10?build=pyhd3eb1b0_0&channel=pkgs/main&subdir=noarch',
                         c_idna.purl.to_string())
        self.assertEqual(1, len(c_idna.external_references), f'{c_idna.external_references}')
        self.assertEqual(0, len(c_idna.external_references.pop().hashes))
        self.assertEqual(0, len(c_idna.hashes), f'{c_idna.hashes}')

    def test_conda_list_json_use_purl_bom_ref(self) -> None:
        conda_list_output_file = os.path.join(os.path.dirname(__file__),
                                              'fixtures/conda-list-output.json')

        with (open(conda_list_output_file, 'r')) as conda_list_output_fh:
            parser = CondaListJsonParser(conda_data=conda_list_output_fh.read(),
                                         use_purl_bom_ref=True)

        self.assertEqual(34, parser.component_count())
        components = parser.get_components()

        c_idna = next(filter(lambda c: c.name == 'idna', components), None)
        self.assertIsNotNone(c_idna)
        self.assertEqual('idna', c_idna.name)
        self.assertEqual(c_idna.purl.to_string(), c_idna.bom_ref.value)
        self.assertEqual('2.10', c_idna.version)
        self.assertEqual('pkg:conda/idna@2.10?build=pyhd3eb1b0_0&channel=pkgs/main&subdir=noarch',
                         c_idna.purl.to_string())
        self.assertEqual(1, len(c_idna.external_references), f'{c_idna.external_references}')
        self.assertEqual(0, len(c_idna.external_references.pop().hashes))
        self.assertEqual(0, len(c_idna.hashes), f'{c_idna.hashes}')

    def test_conda_list_explicit_md5(self) -> None:
        conda_list_output_file = os.path.join(os.path.dirname(__file__),
                                              'fixtures/conda-list-explicit-md5.txt')

        with (open(conda_list_output_file, 'r')) as conda_list_output_fh:
            parser = CondaListExplicitParser(conda_data=conda_list_output_fh.read())

        self.assertEqual(34, parser.component_count())
        components = parser.get_components()

        c_idna = next(filter(lambda c: c.name == 'idna', components), None)
        self.assertIsNotNone(c_idna)
        self.assertEqual('idna', c_idna.name)
        self.assertEqual('2.10', c_idna.version)
        self.assertEqual('pkg:conda/idna@2.10?build=pyhd3eb1b0_0&channel=pkgs/main&subdir=noarch&type=tar.bz2',
                         c_idna.purl.to_string())
        self.assertEqual(1, len(c_idna.external_references), f'{c_idna.external_references}')
        self.assertEqual(0, len(c_idna.external_references.pop().hashes))
        self.assertEqual(1, len(c_idna.hashes), f'{c_idna.hashes}')
        hash: HashType = c_idna.hashes.pop()
        self.assertEqual(HashAlgorithm.MD5, hash.alg)
        self.assertEqual('153ff132f593ea80aae2eea61a629c92', hash.content)

    def test_conda_list_build_number_text(self) -> None:
        conda_list_output_file = os.path.join(os.path.dirname(__file__), 'fixtures/conda-list-build-number-text.txt')

        with (open(conda_list_output_file, 'r')) as conda_list_output_fh:
            parser = CondaListExplicitParser(conda_data=conda_list_output_fh.read())

        self.assertEqual(39, parser.component_count())
        components = parser.get_components()

        c_libgcc_mutex = next(filter(lambda c: c.name == '_libgcc_mutex', components), None)
        self.assertIsNotNone(c_libgcc_mutex)
        self.assertEqual('_libgcc_mutex', c_libgcc_mutex.name)
        self.assertEqual('0.1', c_libgcc_mutex.version)
        self.assertEqual('pkg:conda/_libgcc_mutex@0.1?build=main&channel=pkgs/main&subdir=linux-64&type=conda',
                         c_libgcc_mutex.purl.to_string())
        self.assertEqual(0, len(c_libgcc_mutex.hashes), f'{c_libgcc_mutex.hashes}')

        c_pycparser = next(filter(lambda c: c.name == 'pycparser', components), None)
        self.assertIsNotNone(c_pycparser)
        self.assertEqual('pycparser', c_pycparser.name)
        self.assertEqual('2.21', c_pycparser.version)
        self.assertEqual('pkg:conda/pycparser@2.21?build=pyhd3eb1b0_0&channel=pkgs/main&subdir=noarch&type=conda',
                         c_pycparser.purl.to_string())
        self.assertEqual(0, len(c_pycparser.hashes), f'{c_pycparser.hashes}')

        c_openmp_mutex = next(filter(lambda c: c.name == '_openmp_mutex', components), None)
        self.assertIsNotNone(c_openmp_mutex)
        self.assertEqual('_openmp_mutex', c_openmp_mutex.name)
        self.assertEqual('4.5', c_openmp_mutex.version)
        self.assertEqual('pkg:conda/_openmp_mutex@4.5?build=1_gnu&channel=pkgs/main&subdir=linux-64&type=tar.bz2',
                         c_openmp_mutex.purl.to_string())
        self.assertEqual(0, len(c_openmp_mutex.hashes), f'{c_openmp_mutex.hashes}')

    def test_conda_list_malformed(self) -> None:
        conda_list_output_file = os.path.join(os.path.dirname(__file__), 'fixtures/conda-list-broken.txt')

        with (open(conda_list_output_file, 'r')) as conda_list_output_fh:
            with self.assertRaisesRegex(ValueError, re.compile(r'^unexpected format', re.IGNORECASE)):
                CondaListExplicitParser(conda_data=conda_list_output_fh.read())
