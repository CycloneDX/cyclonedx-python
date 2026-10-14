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

from cyclonedx.model.component import Component, ComponentScope, ComponentType

from cyclonedx_py._internal.pipenv import PipenvBB


class TestPipenvScope(TestCase):

    def setUp(self) -> None:
        self.bb = PipenvBB(logger=logging.getLogger('test-pipenv'), pypi_url=None)

    def test_dev_packages_marked_excluded(self) -> None:
        locker = {
            '_meta': {},
            'default': {'colorama': {'version': '==0.4.6'}},
            'develop': {'arrow': {'version': '==1.3.0'}}
        }
        bom = self.bb._make_bom(None, locker, frozenset({'default', 'develop'}))
        comp_map = {c.name: c for c in bom.components}

        self.assertIn('colorama', comp_map)
        self.assertIsNone(comp_map['colorama'].scope)

        self.assertIn('arrow', comp_map)
        self.assertEqual(ComponentScope.EXCLUDED, comp_map['arrow'].scope)

    def test_package_in_both_default_and_develop_not_excluded(self) -> None:
        locker = {
            '_meta': {},
            'default': {'shared-pkg': {'version': '==1.0.0'}},
            'develop': {
                'shared-pkg': {'version': '==1.0.0'},
                'dev-only': {'version': '==2.0.0'}
            }
        }
        bom = self.bb._make_bom(None, locker, frozenset({'default', 'develop'}))
        comp_map = {c.name: c for c in bom.components}

        self.assertIn('shared-pkg', comp_map)
        self.assertIsNone(comp_map['shared-pkg'].scope)

        self.assertIn('dev-only', comp_map)
        self.assertEqual(ComponentScope.EXCLUDED, comp_map['dev-only'].scope)

    def test_package_normalized_name_matching(self) -> None:
        locker = {
            '_meta': {},
            'default': {'Types_Python_Dateutil': {'version': '==1.0.0'}},
            'develop': {'types-python-dateutil': {'version': '==1.0.0'}}
        }
        bom = self.bb._make_bom(None, locker, frozenset({'default', 'develop'}))
        comp_map = {c.name: c for c in bom.components}

        self.assertEqual(1, len(bom.components))
        comp = next(iter(bom.components))
        self.assertIsNone(comp.scope)

    def test_default_only_groups_leaves_scope_none(self) -> None:
        locker = {
            '_meta': {},
            'default': {'colorama': {'version': '==0.4.6'}},
            'develop': {'arrow': {'version': '==1.3.0'}}
        }
        bom = self.bb._make_bom(None, locker, frozenset({'default'}))
        comp_map = {c.name: c for c in bom.components}

        self.assertIn('colorama', comp_map)
        self.assertIsNone(comp_map['colorama'].scope)
        self.assertNotIn('arrow', comp_map)

    def test_root_component_scope_not_modified(self) -> None:
        root_c = Component(name='my-root-pkg', type=ComponentType.APPLICATION)
        locker = {
            '_meta': {},
            'default': {},
            'develop': {'my-root-pkg': {'version': '==0.1.0'}, 'dev-pkg': {'version': '==1.0.0'}}
        }
        bom = self.bb._make_bom(root_c, locker, frozenset({'default', 'develop'}))
        self.assertIsNone(root_c.scope)
        self.assertIs(root_c, bom.metadata.component)
        comp_map = {c.name: c for c in bom.components}
        self.assertIn('dev-pkg', comp_map)
        self.assertEqual(ComponentScope.EXCLUDED, comp_map['dev-pkg'].scope)

    def test_custom_non_develop_category_not_excluded(self) -> None:
        locker = {
            '_meta': {},
            'docs': {'sphinx': {'version': '==5.0.0'}},
            'develop': {
                'sphinx': {'version': '==5.0.0'},
                'pytest': {'version': '==7.0.0'}
            }
        }
        bom = self.bb._make_bom(None, locker, frozenset({'docs', 'develop'}))
        comp_map = {c.name: c for c in bom.components}

        self.assertIn('sphinx', comp_map)
        self.assertIsNone(comp_map['sphinx'].scope)

        self.assertIn('pytest', comp_map)
        self.assertEqual(ComponentScope.EXCLUDED, comp_map['pytest'].scope)
