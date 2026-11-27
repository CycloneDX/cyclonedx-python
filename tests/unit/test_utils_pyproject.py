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
from typing import Any
from unittest import TestCase

from cyclonedx.model import ExternalReferenceType
from cyclonedx.model.component import ComponentType
from cyclonedx.model.license import DisjunctiveLicense

from cyclonedx_py._internal.utils.pyproject import pyproject2component, pyproject2dependencies


class TestUtilsPyproject(TestCase):

    def setUp(self) -> None:
        self._logger = logging.getLogger('test_utils_pyproject')

    def test_pure_pep621_with_pep639_license(self) -> None:
        data: dict[str, Any] = {
            'project': {
                'name': 'pep621-pkg',
                'version': '2.0.0',
                'description': 'Pure PEP 621 package',
                'license': 'Apache-2.0',
                'urls': {
                    'Homepage': 'https://example.org/pep621-pkg',
                },
            },
        }
        c = pyproject2component(
            data,
            ctype=ComponentType.APPLICATION,
            fpath='pyproject.toml',
            gather_license_texts=False,
            logger=self._logger,
        )
        self.assertEqual('pep621-pkg', c.name)
        self.assertEqual('2.0.0', c.version)
        self.assertEqual('Pure PEP 621 package', c.description)
        licenses = tuple(c.licenses)
        self.assertEqual(1, len(licenses))
        self.assertIsInstance(licenses[0], DisjunctiveLicense)
        assert isinstance(licenses[0], DisjunctiveLicense)
        self.assertEqual('Apache-2.0', licenses[0].id)
        extrefs = {(er.type, er.url.uri) for er in c.external_references}
        self.assertEqual({(ExternalReferenceType.WEBSITE, 'https://example.org/pep621-pkg')}, extrefs)

    def test_hybrid_project_and_poetry_merges_dynamic_and_deduplicates_urls(self) -> None:
        data: dict[str, Any] = {
            'project': {
                'name': 'hybrid-pkg',
                'dynamic': ['version', 'description', 'license'],
                'urls': {
                    'Homepage': 'https://example.org/hybrid',
                },
            },
            'tool': {
                'poetry': {
                    'version': '1.2.3',
                    'description': 'Fallback description from poetry',
                    'license': 'MIT',
                    'homepage': 'https://example.org/hybrid',
                    'repository': 'https://github.com/example/hybrid',
                },
            },
        }
        c = pyproject2component(
            data,
            ctype=ComponentType.LIBRARY,
            fpath='pyproject.toml',
            gather_license_texts=False,
            logger=self._logger,
        )
        self.assertEqual('hybrid-pkg', c.name)
        self.assertEqual('1.2.3', c.version)
        self.assertEqual('Fallback description from poetry', c.description)
        licenses = tuple(c.licenses)
        self.assertEqual(1, len(licenses))
        assert isinstance(licenses[0], DisjunctiveLicense)
        self.assertEqual('MIT', licenses[0].id)
        extrefs = [(er.type, er.url.uri) for er in c.external_references]
        self.assertEqual(2, len(extrefs))
        self.assertIn((ExternalReferenceType.WEBSITE, 'https://example.org/hybrid'), extrefs)
        self.assertIn((ExternalReferenceType.VCS, 'https://github.com/example/hybrid'), extrefs)

    def test_hybrid_pep639_license_ignores_legacy_poetry_license(self) -> None:
        data: dict[str, Any] = {
            'project': {
                'name': 'pep639-hybrid',
                'version': '1.0.0',
                'license': 'MIT',
            },
            'tool': {
                'poetry': {
                    'license': 'Apache-2.0',
                    'classifiers': ['License :: OSI Approved :: BSD License'],
                },
            },
        }
        c = pyproject2component(
            data,
            ctype=ComponentType.APPLICATION,
            fpath='pyproject.toml',
            gather_license_texts=False,
            logger=self._logger,
        )
        licenses = tuple(c.licenses)
        self.assertEqual(1, len(licenses))
        assert isinstance(licenses[0], DisjunctiveLicense)
        self.assertEqual('MIT', licenses[0].id)

    def test_hybrid_pep621_license_does_not_pull_poetry_license(self) -> None:
        data: dict[str, Any] = {
            'project': {
                'name': 'pep621-hybrid',
                'version': '1.0.0',
                'license': {'text': 'MIT'},
            },
            'tool': {
                'poetry': {
                    'license': 'Apache-2.0',
                },
            },
        }
        c = pyproject2component(
            data,
            ctype=ComponentType.APPLICATION,
            fpath='pyproject.toml',
            gather_license_texts=False,
            logger=self._logger,
        )
        licenses = tuple(c.licenses)
        self.assertEqual(1, len(licenses))
        assert isinstance(licenses[0], DisjunctiveLicense)
        self.assertEqual('MIT', licenses[0].id)

    def test_legacy_poetry_only_still_supported(self) -> None:
        data: dict[str, Any] = {
            'tool': {
                'poetry': {
                    'name': 'legacy-pkg',
                    'version': '0.1.0',
                    'license': 'ISC',
                },
            },
        }
        c = pyproject2component(
            data,
            ctype=ComponentType.APPLICATION,
            fpath='pyproject.toml',
            gather_license_texts=False,
            logger=self._logger,
        )
        self.assertEqual('legacy-pkg', c.name)
        self.assertEqual('0.1.0', c.version)

    def test_invalid_empty_pyproject_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, 'Unable to build component from pyproject'):
            pyproject2component(
                {},
                ctype=ComponentType.APPLICATION,
                fpath='pyproject.toml',
                gather_license_texts=False,
                logger=self._logger,
            )

    def test_pyproject2dependencies_combines_project_and_poetry(self) -> None:
        data: dict[str, Any] = {
            'project': {
                'name': 'hybrid-deps',
                'dependencies': ['requests[security] (>=2.28,<3)'],
                'optional-dependencies': {
                    'extra-a': ['tomli (>=2.0)'],
                },
            },
            'tool': {
                'poetry': {
                    'dependencies': {
                        'multi': [
                            {'version': '>=1', 'extras': ['foo']},
                            {'version': '<1', 'extras': ['bar']},
                        ],
                    },
                    'group': {
                        'dev': {
                            'dependencies': {
                                'ddt': '^1.7.2',
                            },
                        },
                    },
                },
            },
        }
        reqs = {req.name: req.extras for req in pyproject2dependencies(data)}
        self.assertEqual({
            'requests': {'security'},
            'tomli': set(),
            'multi': {'foo', 'bar'},
            'ddt': set(),
        }, reqs)

    def test_pyproject2dependencies_empty_returns_empty(self) -> None:
        self.assertEqual([], list(pyproject2dependencies({})))
