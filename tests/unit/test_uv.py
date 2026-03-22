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
from os.path import join
from tempfile import TemporaryDirectory
from unittest import TestCase

from cyclonedx.model.component import ComponentType

from cyclonedx_py._internal.uv import UvBB


class TestUv(TestCase):

    def test_filters_resolution_and_dependency_markers(self) -> None:
        with TemporaryDirectory() as project_dir:
            pyproject = (
                '[project]\n'
                'name = "my-project"\n'
                'version = "0.1.0"\n'
                'dependencies = ["anyio"]\n'
            )
            uv_lock = (
                'version = 1\n'
                'resolution-markers = [\n'
                '  "python_full_version >= \'0\'",\n'
                '  "python_full_version < \'0\'",\n'
                ']\n'
                '\n'
                '[[package]]\n'
                'name = "anyio"\n'
                'version = "1.0.0"\n'
                'dependencies = [\n'
                '  { name = "bar" },\n'
                '  { name = "foo", marker = "python_full_version < \'0\'" },\n'
                ']\n'
                '\n'
                '[[package]]\n'
                'name = "bar"\n'
                'version = "1.0.0"\n'
                'resolution-markers = ["python_full_version >= \'0\'"]\n'
                '\n'
                '[[package]]\n'
                'name = "bar"\n'
                'version = "2.0.0"\n'
                'resolution-markers = ["python_full_version < \'0\'"]\n'
                '\n'
                '[[package]]\n'
                'name = "foo"\n'
                'version = "1.0.0"\n'
            )
            with open(join(project_dir, 'pyproject.toml'), 'w', encoding='utf8', newline='\n') as fh:
                fh.write(pyproject)
            with open(join(project_dir, 'uv.lock'), 'w', encoding='utf8', newline='\n') as fh:
                fh.write(uv_lock)

            bom = UvBB(logger=logging.getLogger(__name__))(
                project_directory=join(project_dir, 'uv.lock'),
                groups_with=[],
                groups_without=[],
                groups_only=[],
                only_dev=False,
                all_groups=False,
                no_default_groups=False,
                no_dev=False,
                extras=[],
                all_extras=False,
                mc_type=ComponentType.APPLICATION,
            )

            components = {(c.name, c.version) for c in bom.components}
            self.assertIn(('anyio', '1.0.0'), components)
            self.assertIn(('bar', '1.0.0'), components)
            self.assertNotIn(('bar', '2.0.0'), components)
            self.assertNotIn(('foo', '1.0.0'), components)

    def test_fails_when_resolution_markers_do_not_match_environment(self) -> None:
        with TemporaryDirectory() as project_dir:
            pyproject = (
                '[project]\n'
                'name = "my-project"\n'
                'version = "0.1.0"\n'
                'dependencies = ["anyio"]\n'
            )
            uv_lock = (
                'version = 1\n'
                'resolution-markers = ["python_full_version < \'0\'"]\n'
                '\n'
                '[[package]]\n'
                'name = "anyio"\n'
                'version = "1.0.0"\n'
            )
            with open(join(project_dir, 'pyproject.toml'), 'w', encoding='utf8', newline='\n') as fh:
                fh.write(pyproject)
            with open(join(project_dir, 'uv.lock'), 'w', encoding='utf8', newline='\n') as fh:
                fh.write(uv_lock)

            with self.assertRaisesRegex(ValueError, 'resolution-markers'):
                UvBB(logger=logging.getLogger(__name__))(
                    project_directory=project_dir,
                    groups_with=[],
                    groups_without=[],
                    groups_only=[],
                    only_dev=False,
                    all_groups=False,
                    no_default_groups=False,
                    no_dev=False,
                    extras=[],
                    all_extras=False,
                    mc_type=ComponentType.APPLICATION,
                )

    def test_dependency_groups(self) -> None:
        with TemporaryDirectory() as project_dir:
            pyproject = (
                '[project]\n'
                'name = "my-project"\n'
                'version = "0.1.0"\n'
                'dependencies = ["requests"]\n'
                '\n'
                '[dependency-groups]\n'
                'dev = [\n'
                '  "pytest",\n'
                '  "mkdocstrings[python]",\n'
                ']\n'
                'docs = ["sphinx"]\n'
            )
            uv_lock = (
                'version = 1\n'
                '\n'
                '[[package]]\n'
                'name = "requests"\n'
                'version = "1.0.0"\n'
                '\n'
                '[[package]]\n'
                'name = "pytest"\n'
                'version = "2.0.0"\n'
                '\n'
                '[[package]]\n'
                'name = "mkdocstrings"\n'
                'version = "3.0.0"\n'
                '\n'
                '[[package]]\n'
                'name = "sphinx"\n'
                'version = "4.0.0"\n'
                '\n'
                '[[package]]\n'
                'name = "my-project"\n'
                'version = "0.1.0"\n'
                'source = { editable = "." }\n'
                'dependencies = [\n'
                '  { name = "requests" },\n'
                ']\n'
                '\n'
                '[package.dev-dependencies]\n'
                'dev = [\n'
                '  { name = "pytest" },\n'
                '  { name = "mkdocstrings", extra = ["python"] },\n'
                ']\n'
            )
            with open(join(project_dir, 'pyproject.toml'), 'w', encoding='utf8', newline='\n') as fh:
                fh.write(pyproject)
            with open(join(project_dir, 'uv.lock'), 'w', encoding='utf8', newline='\n') as fh:
                fh.write(uv_lock)

            components_default = {(c.name, c.version) for c in UvBB(logger=logging.getLogger(__name__))(
                project_directory=project_dir,
                groups_with=[],
                groups_without=[],
                groups_only=[],
                only_dev=False,
                all_groups=False,
                no_default_groups=False,
                no_dev=False,
                extras=[],
                all_extras=False,
                mc_type=ComponentType.APPLICATION,
            ).components}
            self.assertIn(('requests', '1.0.0'), components_default)
            self.assertIn(('pytest', '2.0.0'), components_default)
            self.assertIn(('mkdocstrings', '3.0.0'), components_default)
            self.assertNotIn(('sphinx', '4.0.0'), components_default)

            components_no_dev = {(c.name, c.version) for c in UvBB(logger=logging.getLogger(__name__))(
                project_directory=project_dir,
                groups_with=[],
                groups_without=[],
                groups_only=[],
                only_dev=False,
                all_groups=False,
                no_default_groups=False,
                no_dev=True,
                extras=[],
                all_extras=False,
                mc_type=ComponentType.APPLICATION,
            ).components}
            self.assertIn(('requests', '1.0.0'), components_no_dev)
            self.assertNotIn(('pytest', '2.0.0'), components_no_dev)

            components_docs_only = {(c.name, c.version) for c in UvBB(logger=logging.getLogger(__name__))(
                project_directory=project_dir,
                groups_with=[],
                groups_without=[],
                groups_only=['docs'],
                only_dev=False,
                all_groups=False,
                no_default_groups=False,
                no_dev=False,
                extras=[],
                all_extras=False,
                mc_type=ComponentType.APPLICATION,
            ).components}
            self.assertIn(('sphinx', '4.0.0'), components_docs_only)
            self.assertNotIn(('requests', '1.0.0'), components_docs_only)

            components_only_dev = {(c.name, c.version) for c in UvBB(logger=logging.getLogger(__name__))(
                project_directory=project_dir,
                groups_with=[],
                groups_without=[],
                groups_only=[],
                only_dev=True,
                all_groups=False,
                no_default_groups=False,
                no_dev=False,
                extras=[],
                all_extras=False,
                mc_type=ComponentType.APPLICATION,
            ).components}
            self.assertIn(('pytest', '2.0.0'), components_only_dev)
            self.assertNotIn(('requests', '1.0.0'), components_only_dev)
