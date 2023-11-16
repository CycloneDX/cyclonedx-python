# This file is part of CycloneDX Python Lib
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
from io import StringIO
from os.path import join
from typing import Any
from unittest import TestCase
from unittest.mock import Mock

from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.schema import OutputFormat, SchemaVersion
from ddt import ddt, named_data
from packageurl import PackageURL

from cyclonedx_py._internal import BomBuilder
from cyclonedx_py._internal.cli import Command
from tests import SnapshotMixin


@ddt
class TestCli(TestCase, SnapshotMixin):

    @named_data(('normal', False), ('short', True))
    def test_purls_as_expected(self, short_purls: bool) -> None:
        bom = Bom()
        bom.metadata.component = Component(
            type=ComponentType.APPLICATION,
            name='my-app',
            bom_ref='my-app',
            purl=PackageURL('generic', 'testing', 'my-app', '1', {})
        )
        bom.components.add(Component(
            type=ComponentType.LIBRARY,
            name='my-lib-A',
            bom_ref='my-lib-A',
            purl=PackageURL('generic', 'testing', 'my-lib-A', '2', {'lol': 'rofl'}),
            components=[Component(
                type=ComponentType.APPLICATION,
                name='my-lib-A-sub',
                bom_ref='my-lib-A-sub',
                purl=PackageURL('generic', 'testing', 'my-lib-A-sub', None, 'foo=bar', 'bazz')
            )]
        ))
        bom.serial_number = None
        bom.metadata.timestamp = None
        bom.metadata.tools.clear()

        class MyBBC(BomBuilder):
            def __new__(cls, *args: Any, **kwargs: Any) -> BomBuilder:
                return Mock(spec=BomBuilder, return_value=bom)

        with StringIO() as logs, StringIO() as outs:
            logs.name = '<logstream>'
            outs.name = '<outstream>'

            logger = logging.getLogger('testing')
            logger.propagate = False
            lh = logging.StreamHandler(logs)
            lh.setLevel(logger.level)
            logger.addHandler(lh)

            command = Command(
                logger=logger,
                short_purls=short_purls,
                schema_version=SchemaVersion.V1_4,
                output_format=OutputFormat.JSON,
                should_validate=True,
                _bbc=MyBBC
            )
            command(outfile=outs)

            out = outs.getvalue()

        self.assertEqualSnapshot(out, f'purls-{"short" if short_purls else "normal"}.json')

    def test_validation_throws_with_invalid(self) -> None:
        class MyBBC(BomBuilder):
            def __new__(cls, *args: Any, **kwargs: Any) -> BomBuilder:
                return Mock(spec=BomBuilder, return_value=Mock(spec=Bom))

        with StringIO() as logs, StringIO() as outs:
            logs.name = '<logstream>'
            outs.name = '<outstream>'

            logger = logging.getLogger('testing')
            logger.propagate = False
            lh = logging.StreamHandler(logs)
            lh.setLevel(logger.level)
            logger.addHandler(lh)

            command = Command(
                logger=logger,
                short_purls=False,
                schema_version=SchemaVersion.V1_4,
                output_format=OutputFormat.JSON,
                should_validate=True,
                _bbc=MyBBC
            )
            command._make_output = Mock(return_value='["invalid to CDX schema"]')

            with self.assertRaisesRegex(ValueError, 'is schema-invalid'):
                command(outfile=outs)

    def test_validation_skip_with_invalid(self) -> None:
        class MyBBC(BomBuilder):
            def __new__(cls, *args: Any, **kwargs: Any) -> BomBuilder:
                return Mock(spec=BomBuilder, return_value=Mock(spec=Bom))

        with StringIO() as logs, StringIO() as outs:
            logs.name = '<logstream>'
            outs.name = '<outstream>'

            logger = logging.getLogger('testing')
            logger.level = logging.WARNING
            logger.propagate = False
            lh = logging.StreamHandler(logs)
            lh.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
            lh.setLevel(logger.level)
            logger.addHandler(lh)

            command = Command(
                logger=logger,
                short_purls=False,
                schema_version=SchemaVersion.V1_4,
                output_format=OutputFormat.JSON,
                should_validate=False,
                _bbc=MyBBC
            )
            command._make_output = Mock(return_value='["invalid to CDX schema"]')

            command(outfile=outs)

            log = logs.getvalue()
            out = outs.getvalue()

        self.assertEqual('["invalid to CDX schema"]', out)
        self.assertIn('WARNING: Validation skipped', log)

    def assertEqualSnapshot(self, actual: str, snapshot_name: str) -> None:  # noqa: N802
        super().assertEqualSnapshot(actual, join('cli', snapshot_name))
