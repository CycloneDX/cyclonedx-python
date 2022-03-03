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

import subprocess
import sys
from unittest import TestCase

import cyclonedx_py


class TestCli(TestCase):

    def test_callable_as_module(self) -> None:
        args = [sys.executable, '-m', cyclonedx_py.__name__, '--help']

        # Test whether the call passed, is fair enough for now.
        # Additional tests may come later, to check output etc.
        returncode = subprocess.call(
            args,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            shell=False,
        )

        self.assertEqual(0, returncode, msg='subprocess returned unexpected non-zero')
