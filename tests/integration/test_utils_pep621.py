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

import os
import tempfile
import unittest

from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model.license import DisjunctiveLicense, LicenseAcknowledgement

from cyclonedx_py._internal.utils.pep621 import project2licenses


class TestUtilsPEP621(unittest.TestCase):

    def test_license_dict_text_pep621(self) -> None:
        lfac = LicenseFactory()
        with tempfile.TemporaryDirectory() as tmpdir:
            fpath = tmpdir  # Use the temp directory as the base for any temp files
            project = {
                'name': 'testpkg',
                'license': {'text': 'This is the license text.'},
            }
            licenses = list(project2licenses(project, lfac, fpath=fpath))
            self.assertEqual(len(licenses), 1)
            lic = licenses[0]
            self.assertIsInstance(lic, DisjunctiveLicense)
            self.assertIsNone(lic.id)
            self.assertEqual(lic.text.content, 'This is the license text.')
            self.assertEqual(lic.acknowledgement, LicenseAcknowledgement.DECLARED)

    def test_license_dict_file_pep621(self) -> None:
        lfac = LicenseFactory()
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'license.txt')
            with open(file_path, 'w') as tf:
                tf.write('File license text')
            project = {
                'name': 'testpkg',
                'license': {'file': 'license.txt'},
            }
            licenses = list(project2licenses(project, lfac, fpath=file_path))
            self.assertEqual(len(licenses), 1)
            lic = licenses[0]
            self.assertIsInstance(lic, DisjunctiveLicense)
            self.assertIsNotNone(lic.text.content)
            self.assertEqual(lic.acknowledgement, LicenseAcknowledgement.DECLARED)

    def test_license_non_dict_pep621(self) -> None:
        lfac = LicenseFactory()
        fpath = tempfile.mktemp()

        # Test with string license (should be silently skipped)
        project = {
            'name': 'testpkg',
            'license': 'MIT',
        }
        licenses = list(project2licenses(project, lfac, fpath=fpath))
        self.assertEqual(len(licenses), 0)

        # Test with None license (should be silently skipped)
        project = {
            'name': 'testpkg',
            'license': None,
        }
        licenses = list(project2licenses(project, lfac, fpath=fpath))
        self.assertEqual(len(licenses), 0)

        # Test with list license (should be silently skipped)
        project = {
            'name': 'testpkg',
            'license': ['MIT', 'Apache-2.0'],
        }
        licenses = list(project2licenses(project, lfac, fpath=fpath))
        self.assertEqual(len(licenses), 0)
