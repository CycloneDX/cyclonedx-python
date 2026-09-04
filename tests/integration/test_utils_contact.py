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

from collections.abc import Generator
from unittest import TestCase

from cyclonedx.model.contact import OrganizationalContact
from ddt import ddt, named_data

from cyclonedx_py._internal.utils.contact import contacts2author, person_string2contact


@ddt()
class TestPersonString2Contact(TestCase):

    @named_data(
        ('name_and_email', 'Jane Doe <jane@example.com>', 'Jane Doe', 'jane@example.com'),
        ('name_and_email_extra_whitespace', '  Jane Doe   <jane@example.com>  ', 'Jane Doe', 'jane@example.com'),
        ('name_only', 'Jane Doe', 'Jane Doe', None),
        ('name_only_multiple_words', 'Jane van der Doe', 'Jane van der Doe', None),
        ('email_only', '<jane@example.com>', None, 'jane@example.com'),
        ('email_only_no_angle_brackets_is_a_name', 'jane@example.com', 'jane@example.com', None),
    )
    def test_valid(self, value: str, expected_name: str, expected_email: str) -> None:
        contact = person_string2contact(value)
        self.assertIsInstance(contact, OrganizationalContact)
        self.assertEqual(contact.name, expected_name)
        self.assertEqual(contact.email, expected_email)

    @named_data(
        ('empty_string', ''),
        ('whitespace_only', '   '),
        ('empty_angle_brackets', '<>'),
        ('whitespace_and_empty_angle_brackets', '  <>  '),
    )
    def test_none_for_empty_input(self, value: str) -> None:
        self.assertIsNone(person_string2contact(value))

    @named_data(
        # These do not match `_PERSON_STRING_MATCHER` at all (as opposed to matching
        # and yielding an empty name/email) - regression coverage for the `m is None`
        # branch, which real-world messy author strings can and do reach.
        ('multiple_angle_bracket_fragments', 'Jane <foo> Doe <bar@example.com>'),
        ('trailing_text_after_closing_bracket', 'Jane Doe <jane@example.com> (Acme Inc.)'),
        ('two_email_fragments', 'Jane Doe <jane@example.com><john@example.com>'),
        ('unbalanced_opening_bracket', 'Jane Doe <jane@example.com'),
        ('unbalanced_closing_bracket', 'Jane Doe <jane@example.com>>'),
    )
    def test_none_for_unparseable_shape(self, value: str) -> None:
        self.assertIsNone(person_string2contact(value))


@ddt()
class TestContacts2Author(TestCase):

    def test_empty_iterable_is_none(self) -> None:
        self.assertIsNone(contacts2author(()))

    def test_multiple_contacts_is_none(self) -> None:
        # there is no agreed-upon way to fold multiple authors into one legacy string -
        # see https://github.com/CycloneDX/specification/issues/335
        contacts = (
            OrganizationalContact(name='Jane Doe', email='jane@example.com'),
            OrganizationalContact(name='John Roe', email='john@example.com'),
        )
        self.assertIsNone(contacts2author(contacts))

    @named_data(
        ('name_and_email', OrganizationalContact(name='Jane Doe', email='jane@example.com'),
         'Jane Doe <jane@example.com>'),
        ('name_only', OrganizationalContact(name='Jane Doe'), 'Jane Doe'),
        ('email_only', OrganizationalContact(email='jane@example.com'), 'jane@example.com'),
    )
    def test_single_contact(self, contact: OrganizationalContact, expected: str) -> None:
        self.assertEqual(contacts2author((contact,)), expected)

    def test_single_contact_generator_is_consumed_correctly(self) -> None:
        # `contacts2author()` must work with a one-shot generator, not just a sequence
        def gen() -> Generator[OrganizationalContact, None, None]:
            yield OrganizationalContact(name='Jane Doe', email='jane@example.com')

        self.assertEqual(contacts2author(gen()), 'Jane Doe <jane@example.com>')
