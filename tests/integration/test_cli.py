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


from subprocess import run  # nosec:B404
from sys import executable
from unittest import TestCase

from cyclonedx_py import __version__


class TestPipenv(TestCase):

    def test_call_as_module(self) -> None:
        # show that this thing is callable as a module
        # show that the version is the one expected
        res = run(  # nosec:B603
            (executable, '-m', 'cyclonedx_py', '--version'),
            capture_output=True, encoding='utf8', shell=False)
        self.assertEqual(0, res.returncode, '\n'.join((res.stdout, res.stderr)))
        self.assertIn(__version__, res.stdout)
