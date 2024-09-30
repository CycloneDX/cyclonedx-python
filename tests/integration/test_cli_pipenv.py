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


import random
from glob import glob
from os.path import basename, dirname, join
from typing import Any, Generator
from unittest import TestCase

from cyclonedx.schema import OutputFormat, SchemaVersion
from ddt import ddt, named_data

from tests import INFILES_DIRECTORY, SUPPORTED_OF_SV, SnapshotMixin, make_comparable
from tests.integration import run_cli

lockfiles = glob(join(INFILES_DIRECTORY, 'pipenv', '*', 'Pipfile.lock'))
projectdirs = list(dirname(lockfile) for lockfile in lockfiles)

test_data = tuple(
    (f'{basename(projectdir)}-{sv.name}-{of.name}', projectdir, sv, of)
    for projectdir in projectdirs
    for of, sv in SUPPORTED_OF_SV
)


def test_data_file_filter(s: str) -> Generator[Any, None, None]:
    return ((n, d, sv, of) for n, d, sv, of in test_data if s in n)


@ddt
class TestCliPipenv(TestCase, SnapshotMixin):

    def test_help(self) -> None:
        res, out, err = run_cli('pipenv', '--help')
        self.assertEqual(0, res, '\n'.join((out, err)))

    def test_fails_with_dir_not_found(self) -> None:
        _, projectdir, sv, of = random.choice(test_data)  # nosec B311
        res, out, err = run_cli(
            'pipenv',
            '-vvv',
            '--sv', sv.to_version(),
            '--of', of.name,
            '--outfile=-',
            'something-that-must-not-exist.testing')
        self.assertNotEqual(0, res, err)
        self.assertIn('Could not open lock file: something-that-must-not-exist.testing', err)

    def test_with_pyproject_not_found(self) -> None:
        _, projectdir, sv, of = random.choice(test_data)  # nosec B311
        res, out, err = run_cli(
            'pipenv',
            '-vvv',
            '--sv', sv.to_version(),
            '--of', of.name,
            '--outfile=-',
            '--pyproject=something-that-must-not-exist.testing',
            projectdir)
        self.assertNotEqual(0, res, err)
        self.assertIn('Could not open pyproject file: something-that-must-not-exist.testing', err)

    @named_data(*test_data)
    def test_plain_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
        res, out, err = run_cli(
            'pipenv',
            '-vvv',
            '--sv', sv.to_version(),
            '--of', of.name,
            '--output-reproducible',
            '--outfile=-',
            '--pyproject', join(projectdir, 'pyproject.toml'),
            projectdir)
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'plain', projectdir, sv, of)

    @named_data(*test_data_file_filter('category-deps'))
    def test_with_categories_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
        res, out, err = run_cli(
            'pipenv',
            '-vvv',
            '--sv', sv.to_version(),
            '--of', of.name,
            '--output-reproducible',
            '--outfile=-',
            '--categories', 'categoryB,groupA packages,dev-packages',
            projectdir)
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'some-categories', projectdir, sv, of)

    @named_data(*test_data_file_filter('default-and-dev'))
    def test_with_dev_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
        res, out, err = run_cli(
            'pipenv',
            '-vvv',
            '--sv', sv.to_version(),
            '--of', of.name,
            '--output-reproducible',
            '--outfile=-',
            '--dev',
            projectdir)
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'with-dev', projectdir, sv, of)

    @named_data(*test_data_file_filter('private-packages'))
    def test_with_pypi_mirror_as_expected(self, projectdir: str, sv: SchemaVersion, of: OutputFormat) -> None:
        res, out, err = run_cli(
            'pipenv',
            '-vvv',
            '--sv', sv.to_version(),
            '--of', of.name,
            '--output-reproducible',
            '--outfile=-',
            '--pypi-mirror', 'https://user:password@pypy-mirror.testing.acme.org/simple/',
            projectdir)
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'pypi-mirror', projectdir, sv, of)

    def assertEqualSnapshot(self, actual: str,  # noqa:N802
                            purpose: str,
                            projectdir: str,
                            sv: SchemaVersion,
                            of: OutputFormat
                            ) -> None:
        super().assertEqualSnapshot(
            make_comparable(actual, of),
            join('pipenv', f'{purpose}_{basename(projectdir)}_{sv.to_version()}.{of.name.lower()}')
        )
