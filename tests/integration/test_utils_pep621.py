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
from cyclonedx.model.component import ComponentType
from cyclonedx.model.license import DisjunctiveLicense, LicenseAcknowledgement
from ddt import ddt, named_data

from cyclonedx_py._internal.utils.pep621 import project2authors, project2component, project2licenses


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

    # region project2authors

    def test_project2authors_missing_key(self) -> None:
        project = {'name': 'testpkg'}
        self.assertEqual(list(project2authors(project)), [])

    def test_project2authors_empty_list(self) -> None:
        project = {'name': 'testpkg', 'authors': []}
        self.assertEqual(list(project2authors(project)), [])

    def test_project2authors_name_and_email(self) -> None:
        project = {'name': 'testpkg', 'authors': [{'name': 'Jane Doe', 'email': 'jane@example.com'}]}
        authors = list(project2authors(project))
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].name, 'Jane Doe')
        self.assertEqual(authors[0].email, 'jane@example.com')

    def test_project2authors_name_only(self) -> None:
        project = {'name': 'testpkg', 'authors': [{'name': 'Jane Doe'}]}
        authors = list(project2authors(project))
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].name, 'Jane Doe')
        self.assertIsNone(authors[0].email)

    def test_project2authors_email_only(self) -> None:
        project = {'name': 'testpkg', 'authors': [{'email': 'jane@example.com'}]}
        authors = list(project2authors(project))
        self.assertEqual(len(authors), 1)
        self.assertIsNone(authors[0].name)
        self.assertEqual(authors[0].email, 'jane@example.com')

    def test_project2authors_empty_dict_is_skipped(self) -> None:
        # per spec, at least one of `name`/`email` must be given -
        # but be defensive about a malformed entry with neither.
        project = {'name': 'testpkg', 'authors': [{}]}
        self.assertEqual(list(project2authors(project)), [])

    def test_project2authors_string_entry_not_per_spec_but_tolerated(self) -> None:
        # PEP 621 requires authors to be tables, not strings -- but real-world
        # pyproject.toml files sometimes use Poetry's "Name <email>" string
        # convention here regardless (see tests/_data/infiles/pipenv/no-deps).
        # Must not crash on it.
        project = {'name': 'testpkg', 'authors': ['Jane Doe <jane@example.com>', 'John Roe']}
        authors = list(project2authors(project))
        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0].name, 'Jane Doe')
        self.assertEqual(authors[0].email, 'jane@example.com')
        self.assertEqual(authors[1].name, 'John Roe')
        self.assertIsNone(authors[1].email)

    def test_project2authors_multiple(self) -> None:
        project = {'name': 'testpkg', 'authors': [
            {'name': 'Jane Doe', 'email': 'jane@example.com'},
            {'name': 'John Roe'},
        ]}
        authors = list(project2authors(project))
        self.assertEqual(len(authors), 2)
        self.assertEqual([a.name for a in authors], ['Jane Doe', 'John Roe'])

    # endregion project2authors

    # region project2component -- authors wiring

    def test_project2component_authors_populated(self) -> None:
        project = {'name': 'testpkg', 'authors': [{'name': 'Jane Doe', 'email': 'jane@example.com'}]}
        component = project2component(project, ctype=ComponentType.LIBRARY)
        self.assertEqual(len(component.authors), 1)
        self.assertEqual(next(iter(component.authors)).name, 'Jane Doe')
        # exactly one author -> the legacy singular field is populated too
        self.assertEqual(component.author, 'Jane Doe <jane@example.com>')

    def test_project2component_authors_multiple_no_singular_author(self) -> None:
        project = {'name': 'testpkg', 'authors': [
            {'name': 'Jane Doe'},
            {'name': 'John Roe'},
        ]}
        component = project2component(project, ctype=ComponentType.LIBRARY)
        self.assertEqual(len(component.authors), 2)
        # ambiguous how to join more than one into the legacy singular field -> left unset
        self.assertIsNone(component.author)

    def test_project2component_authors_missing(self) -> None:
        project = {'name': 'testpkg'}
        component = project2component(project, ctype=ComponentType.LIBRARY)
        self.assertEqual(len(component.authors), 0)
        self.assertIsNone(component.author)

    def test_project2component_authors_dynamic_is_not_read(self) -> None:
        # per PEP 621, a field listed in `dynamic` MUST NOT be read from the static pyproject.toml
        project = {
            'name': 'testpkg',
            'dynamic': ['authors'],
            'authors': [{'name': 'Jane Doe'}],
        }
        component = project2component(project, ctype=ComponentType.LIBRARY)
        self.assertEqual(len(component.authors), 0)
        self.assertIsNone(component.author)

    # endregion project2component -- authors wiring
