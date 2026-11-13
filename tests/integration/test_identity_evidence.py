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


from importlib.metadata import PathDistribution
from json import loads as json_loads
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory
from typing import Any
from unittest import TestCase
from unittest.mock import patch

from ddt import data, ddt

from tests import INFILES_DIRECTORY
from tests.integration import run_cli

_BUILDERS = ('environment', 'requirements', 'pipenv', 'poetry')


@ddt
class TestIdentityEvidence(TestCase):

    def setUp(self) -> None:
        temporary_directory = TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        self._directory = Path(temporary_directory.name)
        infiles = Path(INFILES_DIRECTORY)
        pyproject = str(infiles / 'requirements' / 'pyproject.toml')

        dist_info = self._directory / 'example_package-1.2.3.dist-info'
        dist_info.mkdir()
        (dist_info / 'METADATA').write_text(
            'Metadata-Version: 2.1\nName: Example-Package\nVersion: 1.2.3\n', encoding='utf8')
        self._distribution = PathDistribution(dist_info)

        pipenv_project = self._directory / 'pipenv'
        pipenv_project.mkdir()
        copyfile(infiles / 'pipenv' / 'default-and-dev' / 'Pipfile.lock', pipenv_project / 'Pipfile.lock')

        poetry_project = self._directory / 'poetry'
        poetry_project.mkdir()
        poetry_fixture = infiles / 'poetry' / 'main-and-dev'
        # Copy the source manifest directly: fixture symlinks may be checked out
        # as plain files on Windows.
        copyfile(poetry_fixture / 'pyproject-proto.toml', poetry_project / 'pyproject.toml')
        copyfile(poetry_fixture / 'lock21' / 'poetry.lock', poetry_project / 'poetry.lock')

        self._arguments = {
            'environment': ('--pyproject', pyproject),
            'requirements': ('--pyproject', pyproject, str(infiles / 'requirements' / 'frozen.txt')),
            'pipenv': ('--pyproject', pyproject, str(pipenv_project)),
            'poetry': (str(poetry_project),),
        }

    def _run_json(self, builder: str, *, gather: bool = False, schema: str = '1.6') -> dict[str, Any]:
        with patch('cyclonedx_py._internal.environment.distributions', return_value=(self._distribution,)):
            result, output, error = run_cli(
                builder,
                '--of', 'JSON', '--sv', schema, '--output-reproducible', '-o=-',
                *(('--gather-identity-evidence',) if gather else ()),
                *self._arguments[builder],
            )
        self.assertEqual(0, result, error)
        return json_loads(output)

    def _assert_identity(self, component: dict[str, Any], source: str) -> None:
        identities = {identity['field']: identity for identity in component['evidence']['identity']}
        self.assertEqual({'name', 'version'}, identities.keys())
        for field, identity in identities.items():
            with self.subTest(field=field, component=component['name']):
                self.assertEqual(component[field], identity['concludedValue'])
                self.assertNotIn('confidence', identity)
                self.assertEqual([{
                    'technique': 'manifest-analysis', 'confidence': 1, 'value': source,
                }], identity['methods'])

    @data(*_BUILDERS)
    def test_opt_in_records_declared_identity(self, builder: str) -> None:
        bom = self._run_json(builder, gather=True)
        components = bom['components']
        self.assertTrue(components)
        for component in components:
            with self.subTest(component=component['name']):
                if builder == 'requirements':
                    source = f"requirements line {component['bom-ref'].removeprefix('requirements-L')}"
                else:
                    source = {
                        'environment': 'Python distribution metadata',
                        'pipenv': 'Pipfile.lock',
                        'poetry': 'poetry.lock',
                    }[builder]
                self._assert_identity(component, source)
        self._assert_identity(bom['metadata']['component'], 'pyproject.toml')
        previous_evidence = self._run_json(builder)['metadata']['component'].get('evidence', {})
        self.assertEqual(previous_evidence.get('licenses'), bom['metadata']['component']['evidence'].get('licenses'))

    @data(*_BUILDERS)
    def test_default_does_not_add_identity_evidence(self, builder: str) -> None:
        bom = self._run_json(builder)
        for component in (*bom['components'], bom['metadata']['component']):
            with self.subTest(component=component['name']):
                self.assertNotIn('identity', component.get('evidence', {}))

    @data(*_BUILDERS)
    def test_schema_before_identity_support_omits_identity(self, builder: str) -> None:
        bom = self._run_json(builder, gather=True, schema='1.4')
        for component in (*bom['components'], bom['metadata']['component']):
            with self.subTest(component=component['name']):
                self.assertNotIn('identity', component.get('evidence', {}))

    def test_requirements_do_not_conclude_inferred_identity(self) -> None:
        requirements = self._directory / 'requirements.txt'
        requirements.write_text(
            'unpinned>=1.0\nhttps://example.invalid/inferred_package-2.0-py3-none-any.whl\n', encoding='utf8')
        self._arguments['requirements'] = (str(requirements),)

        components = {component['bom-ref']: component for component in self._run_json(
            'requirements', gather=True)['components']}

        unpinned = components['requirements-L1']
        self.assertNotIn('version', unpinned)
        self.assertEqual([{
            'field': 'name',
            'concludedValue': 'unpinned',
            'methods': [{'technique': 'manifest-analysis', 'confidence': 1, 'value': 'requirements line 1'}],
        }], unpinned['evidence']['identity'])
        self.assertNotIn('evidence', components['requirements-L2'])

    def test_pipenv_only_concludes_exact_versions(self) -> None:
        lockfile = self._directory / 'pipenv' / 'Pipfile.lock'
        lockfile.write_text(
            '{"_meta": {"sources": []}, "default": {"unpinned": {}, "ranged": {"version": ">=1.2"}}}',
            encoding='utf8')

        components = self._run_json('pipenv', gather=True)['components']

        self.assertEqual({'unpinned', 'ranged'}, {component['name'] for component in components})
        for component in components:
            with self.subTest(component=component['name']):
                self.assertEqual({'name'}, {identity['field'] for identity in component['evidence']['identity']})
