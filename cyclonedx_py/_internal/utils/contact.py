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

"""
Helpers for turning the free-form "person" data found in `pyproject.toml`,
Poetry manifests and packaging core-metadata into `OrganizationalContact` model instances.
"""

from re import compile as re_compile
from typing import TYPE_CHECKING, Optional

from cyclonedx.model.contact import OrganizationalContact

if TYPE_CHECKING:  # pragma: nocover
    from collections.abc import Iterable

# Matches the "Name <email>" convention used by Poetry's `authors`/`maintainers` lists
# and by packaging core-metadata's free-text `Author`/`Author-email` fields.
# Both the name and the `<email>` part are optional on their own - see `person_string2contact()`.
_PERSON_STRING_MATCHER = re_compile(r'^\s*(?P<name>[^<]*?)\s*(?:<(?P<email>[^<>]*)>)?\s*$')


def person_string2contact(value: str) -> Optional[OrganizationalContact]:
    """
    Parse a free-form ``"Name <email>"`` string - as used by Poetry and by
    packaging core-metadata - into an `OrganizationalContact`.

    The name and the email are each optional on their own: a bare name
    (``"Jane Doe"``), a bare email (``"<jane@example.com>"``) and the
    combined form (``"Jane Doe <jane@example.com>"``) are all valid.

    Returns `None` if `value` carries no usable name or email at all.
    """
    m = _PERSON_STRING_MATCHER.match(value)
    if m is None:  # pragma: nocover  -- the pattern matches any string, including the empty one
        return None
    name = m.group('name') or None
    email = m.group('email') or None
    if name is None and email is None:
        return None
    return OrganizationalContact(name=name, email=email)


def contacts2author(contacts: 'Iterable[OrganizationalContact]') -> Optional[str]:
    """
    Derive the legacy singular `Component.author` string from a set of `OrganizationalContact`.

    CycloneDX 1.6 deprecated the singular free-text `author` in favour of the
    structured, repeatable `authors`. There is no agreed-upon way to fold
    multiple authors back into a single string - see
    https://github.com/CycloneDX/specification/issues/335 - so this
    deliberately does *not* guess a join convention for more than one author.

    Returns the sole author's ``"Name <email>"``/``"Name"``/``"<email>"``
    representation when there is exactly one, else `None`.
    """
    contacts = tuple(contacts)
    if len(contacts) != 1:
        return None
    contact = contacts[0]
    if contact.name and contact.email:
        return f'{contact.name} <{contact.email}>'
    return contact.name or contact.email or None
