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


from json import dumps as json_dumps
from os import getenv
from os.path import dirname, join
from pathlib import Path
from re import sub as re_sub
from sys import stderr
from typing import Union
from unittest import TestCase
from xml.sax.saxutils import escape as xml_escape, quoteattr as xml_quoteattr  # nosec:B406

from cyclonedx.schema import OutputFormat, SchemaVersion

from cyclonedx_py import __version__ as __this_version

RECREATE_SNAPSHOTS = '1' == getenv('CDX_TEST_RECREATE_SNAPSHOTS')
if RECREATE_SNAPSHOTS:
    print('!!! WILL RECREATE ALL SNAPSHOTS !!!', file=stderr)

INIT_TESTBEDS = '1' != getenv('CDX_TEST_SKIP_INIT_TESTBEDS')
if INIT_TESTBEDS:
    print('!!! WILL INIT TESTBEDS !!!', file=stderr)

_TESTDATA_DIRECTORY = join(dirname(__file__), '_data')

INFILES_DIRECTORY = join(_TESTDATA_DIRECTORY, 'infiles')
SNAPSHOTS_DIRECTORY = join(_TESTDATA_DIRECTORY, 'snapshots')

UNSUPPORTED_OF_SV = (
    (OutputFormat.JSON, SchemaVersion.V1_1),
    (OutputFormat.JSON, SchemaVersion.V1_0),
)

SUPPORTED_OF_SV = tuple(
    (of, sv)
    for of in OutputFormat
    for sv in SchemaVersion
    if (of, sv) not in UNSUPPORTED_OF_SV
)


class SnapshotMixin:

    @staticmethod
    def getSnapshotFile(snapshot_name: str) -> str:  # noqa: N802
        return join(SNAPSHOTS_DIRECTORY, f'{snapshot_name}.bin')

    @classmethod
    def writeSnapshot(cls, snapshot_name: str, data: str) -> None:  # noqa: N802
        with open(cls.getSnapshotFile(snapshot_name), 'wt', encoding='utf8', newline='\n') as sf:
            sf.write(data)

    @classmethod
    def readSnapshot(cls, snapshot_name: str) -> str:  # noqa: N802
        with open(cls.getSnapshotFile(snapshot_name), 'rt', encoding='utf8', newline='\n') as sf:
            return sf.read()

    def assertEqualSnapshot(self: Union[TestCase, 'SnapshotMixin'],  # noqa: N802
                            actual: str, snapshot_name: str) -> None:
        if RECREATE_SNAPSHOTS:
            self.writeSnapshot(snapshot_name, actual)
        _omd = self.maxDiff
        _omd = self.maxDiff
        self.maxDiff = None
        try:
            self.assertEqual(actual, self.readSnapshot(snapshot_name))
        finally:
            self.maxDiff = _omd


# region reproducible test results

_root_file_uri = Path(__file__).parent.parent.absolute().as_uri() + '/'
_root_file_uri_xml = xml_escape(_root_file_uri)
_root_file_uri_xml_attr = xml_quoteattr(_root_file_uri)[1:-1]
_root_file_uri_json = json_dumps(_root_file_uri)[1:-1]


def make_xml_comparable(bom: str) -> str:
    bom = bom.replace(_root_file_uri_xml, 'file://.../')
    bom = bom.replace(_root_file_uri_xml_attr, 'file://.../')
    bom = bom.replace(  # replace metadata.tools.version
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-bom</name>\n'
        f'        <version>{__this_version}</version>',
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-bom</name>\n'
        '        <version>thisVersion-testing</version>')
    bom = re_sub(  # replace metadata.tools.version
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-python-lib</name>\n'
        '        <version>.*?</version>',
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-python-lib</name>\n'
        '        <version>libVersion-testing</version>',
        bom)
    bom = re_sub(  # replace metadata.tools.externalReferences
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-python-lib</name>\n'
        r'        <version>(.*?)</version>\n'
        r'        <externalReferences>[\s\S]*?</externalReferences>',
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-python-lib</name>\n'
        r'        <version>\1</version>''\n'
        '        <externalReferences><!-- stripped --></externalReferences>',
        bom)
    return bom


def make_json_comparable(bom: str) -> str:
    bom = bom.replace(_root_file_uri_json, 'file://.../')
    bom = bom.replace(  # replace metadata.tools.version
        '        "name": "cyclonedx-bom",\n'
        '        "vendor": "CycloneDX",\n'
        f'        "version": {json_dumps(__this_version)}',
        '        "name": "cyclonedx-bom",\n'
        '        "vendor": "CycloneDX",\n'
        '        "version": "thisVersion-testing"')
    bom = re_sub(  # replace metadata.tools.version
        '        "name": "cyclonedx-python-lib",\n'
        '        "vendor": "CycloneDX",\n'
        '        "version": ".*?"',
        '        "name": "cyclonedx-python-lib",\n'
        '        "vendor": "CycloneDX",\n'
        '        "version": "libVersion-testing"',
        bom)
    bom = re_sub(  # replace metadata.tools.externalReferences
        r'        "externalReferences": \[[\s\S]*?\],\n'
        '        "name": "cyclonedx-python-lib",\n'
        '        "vendor": "CycloneDX"',
        '        "externalReferences": [   ],\n'
        '        "name": "cyclonedx-python-lib",\n'
        '        "vendor": "CycloneDX"',
        bom)
    return bom


def make_comparable(bom: str, of: OutputFormat) -> str:
    if of is OutputFormat.XML:
        return make_xml_comparable(bom)
    if of is OutputFormat.JSON:
        return make_json_comparable(bom)
    raise NotImplementedError(f'unknown OutputFormat: {of!r}')

# endregion reproducible test results
