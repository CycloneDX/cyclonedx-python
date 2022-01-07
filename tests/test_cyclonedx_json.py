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

from tests.base import BaseJsonTestCase


class TestCycloneDxJson(BaseJsonTestCase):

    def test_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            subprocess.check_output([
                'cyclonedx-py',
                '-e',
                '--format=json',
                '-o', path.join(temp_dir, 'sbom.json'),
            ], shell=False)

    def test_conda_list_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run command to generate latest 1.3 XML SBOM from Requirements File
            subprocess.check_output([
                'cyclonedx-bom',
                '-c',
                '--format=json',
                '-i', path.join(TestCycloneDxJson.FIXTURES_DIRECTORY, 'conda-list-explicit-simple.txt'),
                '-o', path.join(temp_dir, 'sbom.json'),
            ], shell=False)

            with open(path.join(temp_dir, 'sbom.json'), 'r') as f:
                with open(
                        path.join(TestCycloneDxJson.FIXTURES_DIRECTORY, 'bom_v1.3_setuptools-conda.json')
                ) as expected:
                    bom_json = f.read()
                    self.assertValidAgainstSchema(bom_json=bom_json, schema_version=DEFAULT_SCHEMA_VERSION)
                    self.assertEqualJsonBom(
                        a=bom_json, b=expected.read()
                    )

    def test_requirements_txt_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run command to generate latest 1.3 XML SBOM from Requirements File
            subprocess.check_output([
                'cyclonedx-py',
                '-r',
                '--format=json',
                '-i', path.join(TestCycloneDxJson.FIXTURES_DIRECTORY, 'requirements-simple.txt'),
                '-o', path.join(temp_dir, 'sbom.json'),
                '-F',
            ], shell=False)

            with open(path.join(temp_dir, 'sbom.json'), 'r') as f:
                with open(path.join(TestCycloneDxJson.FIXTURES_DIRECTORY, 'bom_v1.3_setuptools.json')) as expected:
                    bom_json = f.read()
                    self.assertValidAgainstSchema(bom_json=bom_json, schema_version=DEFAULT_SCHEMA_VERSION)
                    self.assertEqualJsonBom(
                        a=bom_json, b=expected.read()
                    )

    def test_requirements_txt_file_v1_4(self) -> None:
        self._do_test_requirements_txt_file_for_version(schema_version='1.4')

    def test_requirements_txt_file_v1_3(self) -> None:
        self._do_test_requirements_txt_file_for_version(schema_version='1.3')

    def test_requirements_txt_file_v1_2(self) -> None:
        self._do_test_requirements_txt_file_for_version(schema_version='1.2')

    def test_requirements_txt_file_v1_1(self) -> None:
        self._do_test_requirements_txt_file_schema_version_not_supported(schema_version='1.1')

    def test_requirements_txt_file_v1_0(self) -> None:
        self._do_test_requirements_txt_file_schema_version_not_supported(schema_version='1.0')

    def _do_test_requirements_txt_file_for_version(self, schema_version: str) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run command to generate XML SBOM from Requirements File
            subprocess.check_output(' '.join([
                'cyclonedx-py',
                '-r',
                '--format=json',
                '-i', path.join(TestCycloneDxJson.FIXTURES_DIRECTORY, 'requirements-simple.txt'),
                '--schema-version', schema_version,
                '-o', path.join(temp_dir, 'sbom.json'),
            ]), shell=True)

            with open(path.join(temp_dir, 'sbom.json'), 'r') as f:
                with open(path.join(TestCycloneDxJson.FIXTURES_DIRECTORY,
                                    f'bom_v{schema_version}_setuptools.json')) as expected:
                    bom_json = f.read()
                    self.assertValidAgainstSchema(
                        bom_json=bom_json, schema_version=getattr(SchemaVersion, f'V{schema_version.replace(".", "_")}')
                    )
                    self.assertEqualJsonBom(
                        a=bom_json, b=expected.read()
                    )

    def _do_test_requirements_txt_file_schema_version_not_supported(self, schema_version: str) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run command to generate XML SBOM from Requirements File
            with self.assertRaises(subprocess.CalledProcessError) as e:
                subprocess.check_output(' '.join([
                    'cyclonedx-py',
                    '-r',
                    '--format=json',
                    '-i', path.join(TestCycloneDxJson.FIXTURES_DIRECTORY, 'requirements-simple.txt'),
                    '--schema-version', schema_version,
                    '-o', path.join(temp_dir, 'sbom.json'),
                ]), shell=True)

                self.assertEqual(e.returncode, 2)
