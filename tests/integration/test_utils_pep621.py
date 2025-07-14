# This file is part of CycloneDX Python
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

from os import mkdir
from os.path import join
from tempfile import TemporaryDirectory
from unittest import TestCase

from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model import Encoding
from cyclonedx.model.license import DisjunctiveLicense, LicenseAcknowledgement
from ddt import ddt, named_data

from cyclonedx_py._internal.utils.pep621 import project2licenses


@ddt()
class TestUtilsPEP621(TestCase):

    def test_project2licenses_license_dict_text(self) -> None:
        project = {
            'name': 'testpkg',
            'license': {'text': 'This is the license text.'},
        }
        lfac = LicenseFactory()
        with TemporaryDirectory() as tmpdir:
            licenses = list(project2licenses(project, lfac, True, fpath=join(tmpdir, 'pyproject.toml')))
        self.assertEqual(len(licenses), 1)
        lic = licenses[0]
        self.assertIsInstance(lic, DisjunctiveLicense)
        self.assertIsNone(lic.id)
        self.assertIsNone(lic.text.encoding)
        self.assertEqual(lic.text.content, 'This is the license text.')
        self.assertEqual(lic.acknowledgement, LicenseAcknowledgement.DECLARED)

    def test_project2licenses_license_dict_file(self) -> None:
        project = {
            'name': 'testpkg',
            'license': {'file': 'license.txt'},
        }
        lfac = LicenseFactory()
        with TemporaryDirectory() as tmpdir:
            with open(join(tmpdir, 'license.txt'), 'w') as tf:
                tf.write('File license text')
            licenses = list(project2licenses(project, lfac, True, fpath=join(tmpdir, 'pyproject.toml')))
        self.assertEqual(len(licenses), 1)
        lic = licenses[0]
        self.assertIsInstance(lic, DisjunctiveLicense)
        self.assertIs(lic.text.encoding, Encoding.BASE_64)
        self.assertEqual(lic.text.content, 'RmlsZSBsaWNlbnNlIHRleHQ=')
        self.assertEqual(lic.acknowledgement, LicenseAcknowledgement.DECLARED)

    def test_project2licenses_license_dict_file_in_subfolder(self) -> None:
        project = {
            'name': 'testpkg',
            'license': {'file': 'foo/license.txt'},
        }
        lfac = LicenseFactory()
        with TemporaryDirectory() as tmpdir:
            mkdir(join(tmpdir, 'foo'))
            with open(join(tmpdir, 'foo', 'license.txt'), 'w') as tf:
                tf.write('File license text')
            licenses = list(project2licenses(project, lfac, True, fpath=join(tmpdir, 'pyproject.toml')))
        self.assertEqual(len(licenses), 1)
        lic = licenses[0]
        self.assertIsInstance(lic, DisjunctiveLicense)
        self.assertIs(lic.text.encoding, Encoding.BASE_64)
        self.assertEqual(lic.text.content, 'RmlsZSBsaWNlbnNlIHRleHQ=')
        self.assertEqual(lic.acknowledgement, LicenseAcknowledgement.DECLARED)

    @named_data(
        ('none', None),
        ('string', 'MIT'),
        ('list', ['MIT', 'Apache-2.0'])
    )
    def test_project2licenses_license_non_dict(self, license: any) -> None:
        project = {
            'name': 'testpkg',
            'license': license,
        }
        lfac = LicenseFactory()
        with TemporaryDirectory() as tmpdir:
            licenses = list(project2licenses(project, lfac, True, fpath=join(tmpdir, 'pyproject.toml')))
        self.assertEqual(len(licenses), 0)
