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

from unittest import TestCase

from cyclonedx.model.component import ComponentType
from ddt import ddt, named_data

from cyclonedx_py._internal.utils.poetry import poetry2authors, poetry2component


@ddt()
class TestUtilsPoetry(TestCase):

    # region poetry2authors

    def test_poetry2authors_missing_key(self) -> None:
        poetry = {'name': 'testpkg'}
        self.assertEqual(list(poetry2authors(poetry)), [])

    def test_poetry2authors_empty_list(self) -> None:
        poetry = {'name': 'testpkg', 'authors': []}
        self.assertEqual(list(poetry2authors(poetry)), [])

    @named_data(
        ('name_and_email', 'Jane Doe <jane@example.com>', 'Jane Doe', 'jane@example.com'),
        ('name_only', 'Jane Doe', 'Jane Doe', None),
        ('email_only', '<jane@example.com>', None, 'jane@example.com'),
    )
    def test_poetry2authors_single(self, value: str, expected_name: str, expected_email: str) -> None:
        poetry = {'name': 'testpkg', 'authors': [value]}
        authors = list(poetry2authors(poetry))
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].name, expected_name)
        self.assertEqual(authors[0].email, expected_email)

    def test_poetry2authors_multiple(self) -> None:
        poetry = {'name': 'testpkg', 'authors': [
            'Jane Doe <jane@example.com>',
            'John Roe <john@example.com>',
        ]}
        authors = list(poetry2authors(poetry))
        self.assertEqual(len(authors), 2)
        self.assertEqual([a.name for a in authors], ['Jane Doe', 'John Roe'])

    def test_poetry2authors_blank_entry_is_skipped(self) -> None:
        poetry = {'name': 'testpkg', 'authors': ['Jane Doe', '   ']}
        authors = list(poetry2authors(poetry))
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].name, 'Jane Doe')

    # endregion poetry2authors

    # region poetry2component -- authors wiring

    def test_poetry2component_authors_populated(self) -> None:
        poetry = {'name': 'testpkg', 'authors': ['Jane Doe <jane@example.com>']}
        component = poetry2component(poetry, ctype=ComponentType.LIBRARY)
        self.assertEqual(len(component.authors), 1)
        self.assertEqual(next(iter(component.authors)).name, 'Jane Doe')
        self.assertEqual(component.author, 'Jane Doe <jane@example.com>')

    def test_poetry2component_authors_multiple_no_singular_author(self) -> None:
        poetry = {'name': 'testpkg', 'authors': ['Jane Doe', 'John Roe']}
        component = poetry2component(poetry, ctype=ComponentType.LIBRARY)
        self.assertEqual(len(component.authors), 2)
        self.assertIsNone(component.author)

    def test_poetry2component_authors_missing(self) -> None:
        poetry = {'name': 'testpkg'}
        component = poetry2component(poetry, ctype=ComponentType.LIBRARY)
        self.assertEqual(len(component.authors), 0)
        self.assertIsNone(component.author)

    # endregion poetry2component -- authors wiring
