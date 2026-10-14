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

import logging
from unittest import TestCase

from cyclonedx.model.component import ComponentScope, ComponentType

from cyclonedx_py._internal.poetry import PoetryBB


class TestPoetryComponentScope(TestCase):

    def setUp(self) -> None:
        self.bb = PoetryBB(logger=logging.getLogger('test-poetry'))

    def test_dev_dependencies_marked_excluded(self) -> None:
        project = {
            'tool': {
                'poetry': {
                    'name': 'demo',
                    'version': '1.0.0',
                    'group': {
                        'main': {'dependencies': {'prod-pkg': '1.0'}},
                        'dev': {'dependencies': {'dev-pkg': '1.0'}},
                    },
                    'extras': {}
                }
            }
        }
        locker = {
            'metadata': {'lock-version': '2.0'},
            'package': [
                {'name': 'prod-pkg', 'version': '1.0', 'dependencies': {}},
                {'name': 'dev-pkg', 'version': '1.0', 'dependencies': {}},
            ]
        }
        bom = self.bb._make_bom(
            project=project,
            locker=locker,
            use_groups=frozenset({'main', 'dev'}),
            use_extras=frozenset(),
            mc_type=ComponentType.APPLICATION
        )
        c_prod = next(c for c in bom.components if c.name == 'prod-pkg')
        c_dev = next(c for c in bom.components if c.name == 'dev-pkg')

        self.assertIsNone(c_prod.scope)
        self.assertEqual(ComponentScope.EXCLUDED, c_dev.scope)

    def test_transitive_dev_dependencies_marked_excluded(self) -> None:
        project = {
            'tool': {
                'poetry': {
                    'name': 'demo',
                    'version': '1.0.0',
                    'group': {
                        'dev': {'dependencies': {'pytest': '7.0'}},
                    },
                    'extras': {}
                }
            }
        }
        locker = {
            'metadata': {'lock-version': '2.0'},
            'package': [
                {'name': 'pytest', 'version': '7.0', 'dependencies': {'iniconfig': '1.0'}},
                {'name': 'iniconfig', 'version': '1.0', 'dependencies': {}},
            ]
        }
        bom = self.bb._make_bom(
            project=project,
            locker=locker,
            use_groups=frozenset({'dev'}),
            use_extras=frozenset(),
            mc_type=ComponentType.APPLICATION
        )
        c_pytest = next(c for c in bom.components if c.name == 'pytest')
        c_iniconfig = next(c for c in bom.components if c.name == 'iniconfig')

        self.assertEqual(ComponentScope.EXCLUDED, c_pytest.scope)
        self.assertEqual(ComponentScope.EXCLUDED, c_iniconfig.scope)

    def test_shared_dependency_between_main_and_dev_remains_required(self) -> None:
        project = {
            'tool': {
                'poetry': {
                    'name': 'demo',
                    'version': '1.0.0',
                    'group': {
                        'main': {'dependencies': {'api-server': '1.0'}},
                        'dev': {'dependencies': {'test-tool': '1.0'}},
                    },
                    'extras': {}
                }
            }
        }
        locker = {
            'metadata': {'lock-version': '2.0'},
            'package': [
                {'name': 'api-server', 'version': '1.0', 'dependencies': {'pydantic': '2.0'}},
                {'name': 'test-tool', 'version': '1.0', 'dependencies': {'pydantic': '2.0', 'flake8': '5.0'}},
                {'name': 'pydantic', 'version': '2.0', 'dependencies': {}},
                {'name': 'flake8', 'version': '5.0', 'dependencies': {}},
            ]
        }
        bom = self.bb._make_bom(
            project=project,
            locker=locker,
            use_groups=frozenset({'main', 'dev'}),
            use_extras=frozenset(),
            mc_type=ComponentType.APPLICATION
        )
        c_api = next(c for c in bom.components if c.name == 'api-server')
        c_pydantic = next(c for c in bom.components if c.name == 'pydantic')
        c_test = next(c for c in bom.components if c.name == 'test-tool')
        c_flake = next(c for c in bom.components if c.name == 'flake8')

        self.assertIsNone(c_api.scope)
        self.assertIsNone(c_pydantic.scope)  # Shared dependency remains runtime
        self.assertEqual(ComponentScope.EXCLUDED, c_test.scope)
        self.assertEqual(ComponentScope.EXCLUDED, c_flake.scope)

    def test_legacy_dev_dependencies_category_mapping(self) -> None:
        project = {
            'tool': {
                'poetry': {
                    'name': 'demo',
                    'version': '1.0.0',
                    'group': {
                        'main': {'dependencies': {'prod-lib': '1.0'}},
                        'dev': {'dependencies': {'dev-lib': '1.0'}},
                    },
                    'extras': {}
                }
            }
        }
        locker = {
            'metadata': {'lock-version': '1.1'},
            'package': [
                {'name': 'prod-lib', 'version': '1.0', 'category': 'main', 'dependencies': {}},
                {'name': 'dev-lib', 'version': '1.0', 'category': 'dev', 'dependencies': {}},
            ]
        }
        bom = self.bb._make_bom(
            project=project,
            locker=locker,
            use_groups=frozenset({'main', 'dev'}),
            use_extras=frozenset(),
            mc_type=ComponentType.APPLICATION
        )
        c_prod = next(c for c in bom.components if c.name == 'prod-lib')
        c_dev = next(c for c in bom.components if c.name == 'dev-lib')

        self.assertIsNone(c_prod.scope)
        self.assertEqual(ComponentScope.EXCLUDED, c_dev.scope)
