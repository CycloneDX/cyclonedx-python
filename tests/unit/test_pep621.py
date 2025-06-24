# This file is part of CycloneDX Python
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.

import os
import tempfile
import unittest

from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model.license import DisjunctiveLicense, LicenseAcknowledgement

from cyclonedx_py._internal.utils.pep621 import project2licenses


class TestPEP621(unittest.TestCase):
    def setUp(self):
        self.lfac = LicenseFactory()
        self.fpath = tempfile.mktemp()

    def test_license_dict_text_pep621(self):
        project = {
            'name': 'testpkg',
            'license': {'text': 'This is the license text.'},
        }
        licenses = list(project2licenses(project, self.lfac, fpath=self.fpath))
        self.assertEqual(len(licenses), 1)
        lic = licenses[0]
        self.assertIsInstance(lic, DisjunctiveLicense)
        self.assertIsNone(lic.id)
        self.assertEqual(lic.text.content, 'This is the license text.')
        self.assertEqual(lic.acknowledgement, LicenseAcknowledgement.DECLARED)

    def test_license_dict_file_pep621(self):
        with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
            tf.write('File license text')
            tf.flush()
            project = {
                'name': 'testpkg',
                'license': {'file': os.path.basename(tf.name)},
            }
            # fpath should be the file path so dirname(fpath) resolves to the correct directory
            licenses = list(project2licenses(project, self.lfac, fpath=tf.name))
            self.assertEqual(len(licenses), 1)
            lic = licenses[0]
            self.assertIsInstance(lic, DisjunctiveLicense)
            self.assertIsNotNone(lic.text.content)
            self.assertEqual(lic.acknowledgement, LicenseAcknowledgement.DECLARED)
        os.unlink(tf.name)
