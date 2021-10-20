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

import os.path
import subprocess
import tempfile

from base import BaseXmlTestCase

script_path = os.path.dirname(__file__)

FIXTURES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'fixtures')


class TestCycloneDxXml(BaseXmlTestCase):

    def test_environment(self):
        with tempfile.TemporaryDirectory() as dirname:
            subprocess.check_output([
                'cyclonedx-py',
                '-e',
                '-o', os.path.join(dirname, 'sbom.xml'),
            ])

    def text_conda_list_explicit(self):
        with tempfile.TemporaryDirectory() as dirname:
            # Run command to generate latest 1.3 XML SBOM from Requirements File
            subprocess.check_output([
                'cyclonedx-bom',
                '-c',
                '-i', os.path.join(FIXTURES_DIRECTORY, 'conda-list-explicit-simple.txt'),
                '-o', os.path.join(dirname, 'sbom.xml'),
            ])

            with open(os.path.join(dirname, 'sbom.xml'), 'r') as f, \
                    open(os.path.join(FIXTURES_DIRECTORY, 'bom_v1.3_setuptools.xml')) as expected:
                self.assertEqualXmlBom(f.read(), expected.read(),
                                       namespace='http://cyclonedx.org/schema/bom/1.3')
                f.close()
                expected.close()

    def test_requirements_txt_file(self):
        with tempfile.TemporaryDirectory() as dirname:
            # Run command to generate latest 1.3 XML SBOM from Requirements File
            subprocess.check_output([
                'cyclonedx-py',
                '-r',
                '-i', os.path.join(FIXTURES_DIRECTORY, 'requirements-simple.txt'),
                '-o', os.path.join(dirname, 'sbom.xml'),
            ])

            with open(os.path.join(dirname, 'sbom.xml'), 'r') as f, \
                    open(os.path.join(FIXTURES_DIRECTORY, 'bom_v1.3_setuptools.xml')) as expected:
                self.assertEqualXmlBom(f.read(), expected.read(),
                                       namespace='http://cyclonedx.org/schema/bom/1.3')
                f.close()
                expected.close()

    def test_requirements_txt_file_v1_2(self):
        self._do_test_requirements_txt_file_for_version(schema_version='1.2')

    def test_requirements_txt_file_v1_1(self):
        self._do_test_requirements_txt_file_for_version(schema_version='1.1')

    def test_requirements_txt_file_v1_0(self):
        self._do_test_requirements_txt_file_for_version(schema_version='1.0')

    def _do_test_requirements_txt_file_for_version(self, schema_version: str):
        with tempfile.TemporaryDirectory() as dirname:
            # Run command to generate XML SBOM from Requirements File
            subprocess.check_output([
                'cyclonedx-py',
                '-r',
                '-i', os.path.join(FIXTURES_DIRECTORY, 'requirements-simple.txt'),
                '--schema-version', schema_version,
                '-o', os.path.join(dirname, 'sbom.xml'),
            ])

            with open(os.path.join(dirname, 'sbom.xml'), 'r') as f, \
                    open(os.path.join(FIXTURES_DIRECTORY, 'bom_v{}_setuptools.xml'.format(schema_version))) as expected:
                self.assertEqualXmlBom(f.read(), expected.read(),
                                       namespace='http://cyclonedx.org/schema/bom/{}'.format(schema_version))
                f.close()
                expected.close()
