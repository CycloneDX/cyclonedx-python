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

import os
from unittest import TestCase

from cyclonedx_py.parser.requirements import RequirementsFileParser, RequirementsParser


class TestRequirementsParser(TestCase):

    def test_simple(self) -> None:
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/requirements-simple.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
        components = parser.get_components()

        self.assertFalse(parser.has_warnings(), f'{parser.get_warnings()}')
        self.assertEqual(1, len(components), f'{components}')

    def test_example_1(self) -> None:
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/requirements-example-1.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
        components = parser.get_components()

        self.assertFalse(parser.has_warnings(), f'{parser.get_warnings()}')
        self.assertEqual(3, len(components), f'{components}')

    def test_example_with_comments(self) -> None:
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/requirements-with-comments.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
        components = parser.get_components()

        self.assertFalse(parser.has_warnings(), f'{parser.get_warnings()}')
        self.assertEqual(5, len(components), f'{components}')

    def test_example_multilines_with_comments(self) -> None:
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/requirements-multilines-with-comments.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
        components = parser.get_components()

        self.assertFalse(parser.has_warnings(), f'{parser.get_warnings()}')
        self.assertEqual(1, len(components), f'{components}')

    def test_example_local_packages(self) -> None:
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/requirements-local-and-remote-packages.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
        components = parser.get_components()

        self.assertFalse(parser.has_warnings(), f'{parser.get_warnings()}')
        self.assertEqual(6, len(components), f'{components}')

    def test_example_local_and_nested_packages(self) -> None:
        # RequirementsFileParser can parse nested requirements files,
        # but RequirementsParser cannot.
        parser = RequirementsFileParser(
            requirements_file=os.path.join(os.path.dirname(__file__),
                                           'fixtures/requirements-local-and-remote-packages.txt')
        )
        components = parser.get_components()

        self.assertFalse(parser.has_warnings(), f'{parser.get_warnings()}')
        self.assertEqual(7, len(components), f'{components}')

    def test_example_private_packages(self) -> None:
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/requirements-private-packages.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
        components = parser.get_components()

        self.assertFalse(parser.has_warnings(), f'{parser.get_warnings()}')
        self.assertEqual(1, len(components), f'{components}')

    def test_example_with_urls(self) -> None:
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/requirements-with-urls.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
        components = parser.get_components()

        self.assertFalse(parser.has_warnings(), f'{parser.get_warnings()}')
        self.assertEqual(4, len(components), f'{components}')

    def test_example_with_hashes(self) -> None:
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/requirements-with-hashes.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
        components = parser.get_components()

        self.assertFalse(parser.has_warnings(), f'{parser.get_warnings()}')
        self.assertEqual(5, len(components), f'{components}')

    def test_example_without_pinned_versions_warns(self) -> None:
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/requirements-without-pinned-versions.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
        components = parser.get_components()

        self.assertEqual(2, len(components), f'{components}')
        self.assertTrue(parser.has_warnings(), f'{parser.get_warnings()}')
