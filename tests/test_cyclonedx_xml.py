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

from os import path
import subprocess
import tempfile

from cyclonedx.output import DEFAULT_SCHEMA_VERSION, SchemaVersion

from tests.base import BaseXmlTestCase


class TestCycloneDxXml(BaseXmlTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.FIXTURES_DIRECTORY = path.join(path.dirname(__file__), 'fixtures')

    def test_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            subprocess.check_output([
                'cyclonedx-py',
                '-e',
                '-o', path.join(temp_dir, 'sbom.xml'),
            ], shell=False)

    def test_conda_list_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run command to generate latest 1.3 XML SBOM from Requirements File
            subprocess.check_output([
                'cyclonedx-bom',
                '-c',
                '-i', path.join(TestCycloneDxXml.FIXTURES_DIRECTORY, 'conda-list-explicit-simple.txt'),
                '-o', path.join(temp_dir, 'sbom.xml'),
            ], shell=False)

            with open(path.join(temp_dir, 'sbom.xml'), 'r') as f:
                with open(path.join(TestCycloneDxXml.FIXTURES_DIRECTORY, 'bom_v1.3_setuptools-conda.xml')) as expected:
                    bom_xml = f.read()
                    self.assertValidAgainstSchema(bom_xml=bom_xml, schema_version=DEFAULT_SCHEMA_VERSION)
                    self.assertEqualXmlBom(
                        a=bom_xml, b=expected.read(), namespace='http://cyclonedx.org/schema/bom/1.3'
                    )

    def test_requirements_txt_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run command to generate latest 1.3 XML SBOM from Requirements File
            subprocess.check_output([
                'cyclonedx-py',
                '-r',
                '-i', path.join(TestCycloneDxXml.FIXTURES_DIRECTORY, 'requirements-simple.txt'),
                '-o', path.join(temp_dir, 'sbom.xml'),
                '-F',
            ], shell=False)

            with open(path.join(temp_dir, 'sbom.xml'), 'r') as f:
                with open(path.join(TestCycloneDxXml.FIXTURES_DIRECTORY, 'bom_v1.3_setuptools.xml')) as expected:
                    bom_xml = f.read()
                    self.assertValidAgainstSchema(bom_xml=bom_xml, schema_version=DEFAULT_SCHEMA_VERSION)
                    self.assertEqualXmlBom(
                        a=bom_xml, b=expected.read(), namespace='http://cyclonedx.org/schema/bom/1.3'
                    )

    def test_requirements_txt_file_v1_4(self) -> None:
        self._do_test_requirements_txt_file_for_version(schema_version='1.4')

    def test_requirements_txt_file_v1_3(self) -> None:
        self._do_test_requirements_txt_file_for_version(schema_version='1.3')

    def test_requirements_txt_file_v1_2(self) -> None:
        self._do_test_requirements_txt_file_for_version(schema_version='1.2')

    def test_requirements_txt_file_v1_1(self) -> None:
        self._do_test_requirements_txt_file_for_version(schema_version='1.1')

    def test_requirements_txt_file_v1_0(self) -> None:
        self._do_test_requirements_txt_file_for_version(schema_version='1.0')

    def _do_test_requirements_txt_file_for_version(self, schema_version: str) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run command to generate XML SBOM from Requirements File
            subprocess.check_output([
                'cyclonedx-py',
                '-r',
                '-i', path.join(TestCycloneDxXml.FIXTURES_DIRECTORY, 'requirements-simple.txt'),
                '--schema-version', schema_version,
                '-o', path.join(temp_dir, 'sbom.xml'),
            ], shell=False)

            with open(path.join(temp_dir, 'sbom.xml'), 'r') as f:
                with open(path.join(TestCycloneDxXml.FIXTURES_DIRECTORY,
                                    f'bom_v{schema_version}_setuptools.xml')) as expected:
                    bom_xml = f.read()
                    self.assertValidAgainstSchema(
                        bom_xml=bom_xml, schema_version=getattr(SchemaVersion, f'V{schema_version.replace(".", "_")}')
                    )
                    self.assertEqualXmlBom(
                        a=bom_xml, b=expected.read(), namespace=f'http://cyclonedx.org/schema/bom/{schema_version}'
                    )
