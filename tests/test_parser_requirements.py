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
import unittest
from unittest import TestCase

from cyclonedx.parser.requirements import RequirementsParser


class TestRequirementsParser(TestCase):

    def test_simple(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/requirements-simple.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
            r.close()
        self.assertTrue(1, parser.component_count())
        self.assertFalse(parser.has_warnings())

    def test_example_1(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/requirements-example-1.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
            r.close()
        self.assertTrue(3, parser.component_count())
        self.assertFalse(parser.has_warnings())

    def test_example_with_comments(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/requirements-with-comments.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
            r.close()
        self.assertTrue(5, parser.component_count())
        self.assertFalse(parser.has_warnings())

    def test_example_multiline_with_comments(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/requirements-multilines-with-comments.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
            r.close()
        self.assertTrue(5, parser.component_count())
        self.assertFalse(parser.has_warnings())

    @unittest.skip('Not yet supported')
    def test_example_with_hashes(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/requirements-with-hashes.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
            r.close()
        self.assertTrue(5, parser.component_count())
        self.assertFalse(parser.has_warnings())

    def test_example_without_pinned_versions(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/requirements-without-pinned-versions.txt')) as r:
            parser = RequirementsParser(
                requirements_content=r.read()
            )
            r.close()
        self.assertTrue(2, parser.component_count())
        self.assertTrue(parser.has_warnings())
        self.assertEqual(3, len(parser.get_warnings()))
