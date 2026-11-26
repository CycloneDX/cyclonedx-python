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


from json import loads as json_loads
from os.path import join
from tempfile import TemporaryDirectory
from textwrap import dedent
from typing import Any
from unittest import TestCase

from tests.integration import run_cli


class TestPoetryMultiConstraintLockDependencies(TestCase):

    @staticmethod
    def _run_poetry_json(pyproject_toml: str, poetry_lock: str, *extra_args: str) -> dict[str, Any]:
        with TemporaryDirectory() as tmpdir:
            with open(join(tmpdir, 'pyproject.toml'), 'w', encoding='utf8') as f:
                f.write(dedent(pyproject_toml))
            with open(join(tmpdir, 'poetry.lock'), 'w', encoding='utf8') as f:
                f.write(dedent(poetry_lock))
            res, out, err = run_cli(
                'poetry',
                *extra_args,
                '--of', 'JSON',
                '--output-reproducible',
                '-o=-',
                tmpdir,
            )
            if res != 0:
                raise AssertionError(f'CLI failed ({res}): {err}')
            result: dict[str, Any] = json_loads(out)
            return result

    def test_multi_constraint_all_optional_excluded_when_extra_unused(self) -> None:
        pyproject_toml = """\
            [tool.poetry]
            name = "demo"
            version = "0.1.0"
            description = ""
            authors = ["Example <dev@example.com>"]

            [tool.poetry.dependencies]
            python = "^3.11"
            ray = "2.42.1"

            [tool.poetry.group.dev.dependencies]
            ray = { version = "2.42.1", extras = ["serve"] }
            """
        poetry_lock = """\
            [[package]]
            name = "ray"
            version = "2.42.1"
            description = ""
            optional = false
            python-versions = ">=3.9"
            groups = ["main", "dev"]
            files = []

            [package.dependencies]
            click = ">=7.0"
            py-spy = [
                {version = ">=0.2.0", optional = true, markers = 'python_version < "3.12" and extra == "serve"'},
                {version = ">=0.4.0", optional = true, markers = 'python_version >= "3.12" and extra == "serve"'},
            ]

            [package.extras]
            serve = [
                'py-spy (>=0.2.0) ; python_version < "3.12"',
                'py-spy (>=0.4.0) ; python_version >= "3.12"',
            ]

            [[package]]
            name = "click"
            version = "8.1.8"
            description = ""
            optional = false
            python-versions = ">=3.7"
            groups = ["main", "dev"]
            files = []

            [[package]]
            name = "py-spy"
            version = "0.4.0"
            description = ""
            optional = true
            python-versions = ">=3.8"
            groups = ["dev"]
            files = []

            [metadata]
            lock-version = "2.1"
            python-versions = "^3.11"
            content-hash = "0000000000000000000000000000000000000000000000000000000000000000"
            """
        bom_main = self._run_poetry_json(pyproject_toml, poetry_lock, '--only', 'main')
        comp_refs_main = {c['bom-ref'] for c in bom_main.get('components', ())}
        self.assertEqual({'ray@2.42.1', 'click@8.1.8'}, comp_refs_main)
        ray_deps_main = next(d for d in bom_main['dependencies'] if d['ref'] == 'ray@2.42.1')
        self.assertEqual(['click@8.1.8'], ray_deps_main.get('dependsOn', []))

        bom_all = self._run_poetry_json(pyproject_toml, poetry_lock)
        comp_refs_all = {c['bom-ref'] for c in bom_all.get('components', ())}
        self.assertEqual({'ray@2.42.1', 'click@8.1.8', 'py-spy@0.4.0'}, comp_refs_all)
        ray_deps_all = next(d for d in bom_all['dependencies'] if d['ref'] == 'ray@2.42.1')
        self.assertEqual({'click@8.1.8', 'py-spy@0.4.0'}, set(ray_deps_all.get('dependsOn', [])))

    def test_multi_constraint_mixed_optional_and_required_included(self) -> None:
        pyproject_toml = """\
            [tool.poetry]
            name = "demo"
            version = "0.1.0"
            description = ""
            authors = ["Example <dev@example.com>"]

            [tool.poetry.dependencies]
            python = "^3.11"
            parent-pkg = "1.0.0"
            """
        poetry_lock = """\
            [[package]]
            name = "parent-pkg"
            version = "1.0.0"
            description = ""
            optional = false
            python-versions = ">=3.9"
            groups = ["main"]
            files = []

            [package.dependencies]
            helper-pkg = [
                {version = ">=1.0", optional = true, markers = 'python_version < "3.12" and extra == "fast"'},
                {version = ">=2.0", markers = 'python_version >= "3.12"'},
            ]

            [[package]]
            name = "helper-pkg"
            version = "2.0.0"
            description = ""
            optional = false
            python-versions = ">=3.9"
            groups = ["main"]
            files = []

            [metadata]
            lock-version = "2.1"
            python-versions = "^3.11"
            content-hash = "0000000000000000000000000000000000000000000000000000000000000000"
            """
        bom = self._run_poetry_json(pyproject_toml, poetry_lock)
        comp_refs = {c['bom-ref'] for c in bom.get('components', ())}
        self.assertEqual({'parent-pkg@1.0.0', 'helper-pkg@2.0.0'}, comp_refs)

    def test_multi_constraint_extras_propagated_transitively(self) -> None:
        pyproject_toml = """\
            [tool.poetry]
            name = "demo"
            version = "0.1.0"
            description = ""
            authors = ["Example <dev@example.com>"]

            [tool.poetry.dependencies]
            python = "^3.11"
            app-lib = "^1.0.0"
            """
        poetry_lock = """\
            [[package]]
            name = "app-lib"
            version = "1.0.0"
            description = ""
            optional = false
            python-versions = ">=3.10"
            groups = ["main"]
            files = []

            [package.dependencies]
            httpx = [
                {version = ">=0.26", extras = ["http2"], markers = 'python_version < "3.12"'},
                {version = ">=0.27", extras = ["http2", "socks"], markers = 'python_version >= "3.12"'},
            ]

            [[package]]
            name = "httpx"
            version = "0.26.0"
            description = ""
            optional = false
            python-versions = ">=3.8"
            groups = ["main"]
            markers = 'python_version < "3.12"'
            files = []

            [package.extras]
            http2 = ["h2 (>=4.0)"]
            socks = ["socksio (>=1.0)"]

            [[package]]
            name = "httpx"
            version = "0.27.0"
            description = ""
            optional = false
            python-versions = ">=3.8"
            groups = ["main"]
            markers = 'python_version >= "3.12"'
            files = []

            [package.extras]
            http2 = ["h2 (>=4.0)"]
            socks = ["socksio (>=1.0)"]

            [[package]]
            name = "h2"
            version = "4.1.0"
            description = ""
            optional = true
            python-versions = ">=3.8"
            groups = ["main"]
            files = []

            [[package]]
            name = "socksio"
            version = "1.0.0"
            description = ""
            optional = true
            python-versions = ">=3.8"
            groups = ["main"]
            files = []

            [metadata]
            lock-version = "2.1"
            python-versions = "^3.11"
            content-hash = "0000000000000000000000000000000000000000000000000000000000000000"
            """
        bom = self._run_poetry_json(pyproject_toml, poetry_lock)
        comp_refs = {c['bom-ref'] for c in bom.get('components', ())}
        self.assertEqual(
            {'app-lib@1.0.0', 'httpx@0.26.0', 'httpx@0.27.0#1', 'h2@4.1.0', 'socksio@1.0.0'},
            comp_refs,
        )
        for httpx_ref in ('httpx@0.26.0', 'httpx@0.27.0#1'):
            httpx_comp = next(c for c in bom['components'] if c['bom-ref'] == httpx_ref)
            extra_props = {
                p['value'] for p in httpx_comp.get('properties', ())
                if p['name'] == 'cdx:python:package:required-extra'
            }
            self.assertEqual({'http2', 'socks'}, extra_props)
            httpx_deps = next(d for d in bom['dependencies'] if d['ref'] == httpx_ref)
            self.assertEqual({'h2@4.1.0', 'socksio@1.0.0'}, set(httpx_deps.get('dependsOn', ())))
