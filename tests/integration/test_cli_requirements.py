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


import os
import random
from collections.abc import Generator
from glob import glob
from os.path import basename, join, splitext
from typing import Any
from unittest import TestCase

from cyclonedx.schema import OutputFormat, SchemaVersion
from ddt import ddt, named_data

from tests import INFILES_DIRECTORY, SUPPORTED_OF_SV, SnapshotMixin, make_comparable
from tests.integration import run_cli

infiles = glob(join(INFILES_DIRECTORY, 'requirements', '*.txt*'))

pyproject_file = join(INFILES_DIRECTORY, 'requirements', 'pyproject.toml')

test_data = tuple(
    (f'{splitext(basename(infile))[0]}-{sv.name}-{of.name}', infile, sv, of)
    for infile in infiles
    for of, sv in SUPPORTED_OF_SV
)


def test_data_file_filter(s: str) -> Generator[Any, None, None]:
    return ((n, d, sv, of) for n, d, sv, of in test_data if s in n)


if os.name == 'nt':
    def test_data_os_filter(data: Any) -> bool:
        return True
else:
    def test_data_os_filter(data: tuple[Any, str, Any, Any]) -> bool:
        # skip windows encoded files on non-windows
        return '.cp125' not in data[1]


@ddt
class TestCliRequirements(TestCase, SnapshotMixin):

    def test_help(self) -> None:
        res, out, err = run_cli('requirements', '--help')
        self.assertEqual(0, res, '\n'.join((out, err)))

    def test_with_file_not_found(self) -> None:
        _, infile, sv, of = random.choice(test_data)  # nosec B311
        res, out, err = run_cli(
            'requirements',
            '-vvv',
            '--sv', sv.to_version(),
            '--of', of.name,
            '-o=-',
            'something-that-must-not-exist.testing')
        self.assertNotEqual(0, res, err)
        self.assertIn('Could not open requirements file: something-that-must-not-exist.testing', err)

    def test_with_pyproject_not_found(self) -> None:
        _, infile, sv, of = random.choice(test_data)  # nosec B311
        res, out, err = run_cli(
            'requirements',
            '-vvv',
            '--sv', sv.to_version(),
            '--of', of.name,
            '-o=-',
            '--pyproject=something-that-must-not-exist.testing',
            infile
        )
        self.assertNotEqual(0, res, err)
        self.assertIn('Could not open pyproject file: something-that-must-not-exist.testing', err)

    @named_data(*filter(test_data_os_filter, test_data))
    def test_with_file_as_expected(self, infile: str, sv: SchemaVersion, of: OutputFormat) -> None:
        res, out, err = run_cli(
            'requirements',
            '-vvv',
            '--sv', sv.to_version(),
            '--of', of.name,
            '--output-reproducible',
            '-o=-',
            '--pyproject', pyproject_file,
            infile)
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'file', infile, sv, of)

    @named_data(*test_data)
    def test_with_stream_as_expected(self, infile: str, sv: SchemaVersion, of: OutputFormat) -> None:
        with open(infile, 'rb') as inp:
            res, out, err = run_cli(
                'requirements',
                '-vvv',
                '--sv', sv.to_version(),
                '--of', of.name,
                '--output-reproducible',
                '-o=-',
                # no pyproject for this case
                '-',
                inp=inp)
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'stream', infile, sv, of)

    @named_data(*test_data_file_filter('frozen'))
    def test_with_index_auth(self, infile: str, sv: SchemaVersion, of: OutputFormat) -> None:
        res, out, err = run_cli(
            'requirements',
            '-vvv',
            '--index-url', 'https://user:password@pypackages.acme.org/simple/',
            '--extra-index-url', 'https://user:password@legacy1.pypackages.acme.org/simple/',
            '--extra-index-url', 'https://user:password@legacy2.pypackages.acme.org/simple/',
            '--sv', sv.to_version(),
            '--of', of.name,
            '--output-reproducible',
            '-o=-',
            '--pyproject', pyproject_file,
            infile)
        self.assertEqual(0, res, err)
        self.assertEqualSnapshot(out, 'index_auth', infile, sv, of)

    def assertEqualSnapshot(self, actual: str,  # noqa:N802
                            purpose: str,
                            reqfile: str,
                            sv: SchemaVersion,
                            of: OutputFormat
                            ) -> None:
        super().assertEqualSnapshot(
            make_comparable(actual, of),
            join('requirements', f'{purpose}_{splitext(basename(reqfile))[0]}_{sv.to_version()}.{of.name.lower()}')
        )
