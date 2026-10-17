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

from os import environ
from unittest import TestCase
from unittest.mock import patch

from cyclonedx_py._internal.environment import _ISOLATED_ENV_NAMES, _path_probe_env


class TestPathProbeEnv(TestCase):

    def test_default_inherits_parent_environment(self) -> None:
        self.assertIsNone(_path_probe_env(False))

    def test_isolated_drops_discovery_variables_regardless_of_case(self) -> None:
        with patch.dict(environ, {
            'PythonPath': r'C:\leak',
            'PYTHONHOME': r'C:\pyhome',
            'virtual_env': r'C:\venv',
            'PATH': environ.get('PATH', ''),
        }, clear=False):
            env = _path_probe_env(True)

        if env is None:
            self.fail('isolated probe must build an environment')
        folded = {key.casefold() for key in env}
        for name in _ISOLATED_ENV_NAMES:
            self.assertNotIn(name.casefold(), folded)
        self.assertIn('path', folded)
