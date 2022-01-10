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

from unittest import TestCase

from cyclonedx.parser.environment import EnvironmentParser
from cyclonedx.model.component import Component


class TestEnvironmentParser(TestCase):

    def test_simple(self) -> None:
        """
        @todo This test is a vague as it will detect the unique environment where tests are being executed -
                so is this valid?

        :return:
        """
        parser = EnvironmentParser()
        self.assertGreater(parser.component_count(), 1)

        # We can only be sure that tox is in the environment, for example as we use tox to run tests
        c_tox: Component = [x for x in parser.get_components() if x.name == 'tox'][0]
        self.assertIsNotNone(c_tox.licenses)
        self.assertEqual('MIT', c_tox.licenses[0].expression)
