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

from email.message import Message
from typing import Optional
from unittest import TestCase

from ddt import ddt, named_data

from cyclonedx_py._internal.utils.packaging import metadata2authors


def _make_metadata(author: Optional[str] = None, author_email: Optional[str] = None) -> Message:
    metadata = Message()
    if author is not None:
        metadata['Author'] = author
    if author_email is not None:
        metadata['Author-email'] = author_email
    return metadata


@ddt()
class TestMetadata2Authors(TestCase):

    def test_neither_field_present(self) -> None:
        metadata = _make_metadata()
        self.assertEqual(list(metadata2authors(metadata)), [])

    def test_author_only(self) -> None:
        metadata = _make_metadata(author='Jane Doe')
        authors = list(metadata2authors(metadata))
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].name, 'Jane Doe')
        self.assertIsNone(authors[0].email)

    def test_author_email_only_single_address(self) -> None:
        metadata = _make_metadata(author_email='jane@example.com')
        authors = list(metadata2authors(metadata))
        self.assertEqual(len(authors), 1)
        self.assertIsNone(authors[0].name)
        self.assertEqual(authors[0].email, 'jane@example.com')

    def test_author_email_with_display_name(self) -> None:
        # the display name is encoded in the address itself here, `Author` is unused/absent
        metadata = _make_metadata(author_email='Jane Doe <jane@example.com>')
        authors = list(metadata2authors(metadata))
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].name, 'Jane Doe')
        self.assertEqual(authors[0].email, 'jane@example.com')

    def test_author_and_bare_email_are_combined_into_one_contact(self) -> None:
        # the classic split-across-two-fields case: `Author` carries the name,
        # `Author-email` carries a single address with no display name of its own.
        metadata = _make_metadata(author='Jane Doe', author_email='jane@example.com')
        authors = list(metadata2authors(metadata))
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].name, 'Jane Doe')
        self.assertEqual(authors[0].email, 'jane@example.com')

    def test_author_ignored_when_author_email_already_has_a_display_name(self) -> None:
        # combining would silently discard/override one of the two names - refuse to guess.
        metadata = _make_metadata(author='Jane Doe', author_email='Someone Else <jane@example.com>')
        authors = list(metadata2authors(metadata))
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].name, 'Someone Else')
        self.assertEqual(authors[0].email, 'jane@example.com')

    def test_author_ignored_when_it_already_looks_like_an_email(self) -> None:
        # `Author` itself already contains `<...>`/`@` - it is not a "bare name" to combine.
        metadata = _make_metadata(author='Jane Doe <jane@example.com>', author_email='jane@example.com')
        authors = list(metadata2authors(metadata))
        self.assertEqual(len(authors), 1)
        self.assertIsNone(authors[0].name)
        self.assertEqual(authors[0].email, 'jane@example.com')

    def test_multiple_addresses_are_independent_contacts_author_ignored(self) -> None:
        metadata = _make_metadata(
            author='Jane Doe, John Roe',
            author_email='Jane Doe <jane@example.com>, John Roe <john@example.com>',
        )
        authors = list(metadata2authors(metadata))
        self.assertEqual(len(authors), 2)
        self.assertEqual(
            [(a.name, a.email) for a in authors],
            [('Jane Doe', 'jane@example.com'), ('John Roe', 'john@example.com')],
        )

    def test_multiple_addresses_no_display_names(self) -> None:
        metadata = _make_metadata(author_email='jane@example.com, john@example.com')
        authors = list(metadata2authors(metadata))
        self.assertEqual(len(authors), 2)
        self.assertEqual([a.email for a in authors], ['jane@example.com', 'john@example.com'])

    @named_data(
        ('bare_name_no_at_sign', 'Jane Doe'),
        ('multiple_bare_names', 'Jane Doe, John Roe'),
    )
    def test_author_email_that_is_not_actually_an_email_is_discarded(self, bad_value: str) -> None:
        # `email.utils.getaddresses()` mis-splits a bare name on whitespace and would
        # otherwise silently emit a corrupted "address" (e.g. only the last word) -
        # entries without an `@` must be dropped rather than trusted.
        metadata = _make_metadata(author_email=bad_value)
        self.assertEqual(list(metadata2authors(metadata)), [])

    def test_author_used_as_fallback_when_author_email_is_garbage(self) -> None:
        metadata = _make_metadata(author='Jane Doe', author_email='not-an-email-address')
        # the garbage `Author-email` yields zero valid addresses, so the "combine" path
        # never triggers (needs exactly one) - and there is no fallback to `Author`
        # once `Author-email` was present at all, by design (see function docstring).
        self.assertEqual(list(metadata2authors(metadata)), [])

    def test_empty_string_fields_are_treated_as_absent(self) -> None:
        metadata = _make_metadata(author='', author_email='')
        self.assertEqual(list(metadata2authors(metadata)), [])
