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

import sys
from json import dumps as json_dumps
from os import getenv, path
from pathlib import Path
from re import sub as re_sub
from typing import Any, Dict, Union
from unittest import TestCase
from xml.sax.saxutils import escape as xml_escape, quoteattr as xml_quoteattr  # nosec:B406

from cyclonedx.schema import OutputFormat, SchemaVersion

from cyclonedx_py import __version__ as __this_version

RECREATE_SNAPSHOTS = '1' == getenv('CDX_TEST_RECREATE_SNAPSHOTS')
if RECREATE_SNAPSHOTS:
    print('!!! WILL RECREATE ALL SNAPSHOTS !!!', file=sys.stderr)

INIT_TESTBEDS = '1' != getenv('CDX_TEST_SKIP_INIT_TESTBEDS')
if INIT_TESTBEDS:
    print('!!! WILL INIT TESTBEDS !!!', file=sys.stderr)

_TESTDATA_DIRECTORY = path.join(path.dirname(__file__), '_data')

INFILES_DIRECTORY = path.join(_TESTDATA_DIRECTORY, 'infiles')
SNAPSHOTS_DIRECTORY = path.join(_TESTDATA_DIRECTORY, 'snapshots')

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
        return path.join(SNAPSHOTS_DIRECTORY, f'{snapshot_name}.bin')

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

# package is called 'cyclonedx-bom', but the tool is called 'cyclonedx-py'
EXPECTED_TOOL_NAME = 'cyclonedx-py'


def make_xml_comparable(bom: str) -> str:
    bom = bom.replace(_root_file_uri_xml, 'file://.../')
    bom = bom.replace(_root_file_uri_xml_attr, 'file://.../')
    bom = bom.replace(  # replace this version in metadata.tools.components
        '          <group>CycloneDX</group>\n'
        f'          <name>{EXPECTED_TOOL_NAME}</name>\n'
        f'          <version>{__this_version}</version>',
        '          <group>CycloneDX</group>\n'
        f'          <name>{EXPECTED_TOOL_NAME}</name>\n'
        '          <version>thisVersion-testing</version>')
    bom = bom.replace(  # replace this version in metadata.tools
        '        <vendor>CycloneDX</vendor>\n'
        f'        <name>{EXPECTED_TOOL_NAME}</name>\n'
        f'        <version>{__this_version}</version>',
        '        <vendor>CycloneDX</vendor>\n'
        f'        <name>{EXPECTED_TOOL_NAME}</name>\n'
        '        <version>thisVersion-testing</version>')
    bom = re_sub(  # replace lib-dynamics in metadata.tools.components
        '          <group>CycloneDX</group>\n'
        '          <name>cyclonedx-python-lib</name>\n'
        '          <version>.*?</version>\n'
        '          <description>.*?</description>\n'
        '          <licenses>\n'
        '(?:            .*?\n)*'
        '          </licenses>\n'
        '          <externalReferences>\n'
        '(?:            .*?\n)*'
        '          </externalReferences>',
        '          <group>CycloneDX</group>\n'
        '          <name>cyclonedx-python-lib</name>\n'
        '          <version>libVersion-testing</version>\n'
        '          <description><!-- stripped --></description>\n'
        '          <licenses><!-- stripped --></licenses>\n'
        '          <externalReferences><!-- stripped --></externalReferences>',
        bom)
    bom = re_sub(  # replace lib-dynamics version in metadata.tools[]
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-python-lib</name>\n'
        '        <version>.*?</version>',
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-python-lib</name>\n'
        '        <version>libVersion-testing</version>',
        bom)
    bom = re_sub(  # replace lib-dynamics externalReferences in metadata.tools[]
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-python-lib</name>\n'
        '        <version>(.*?)</version>\n'
        '        <externalReferences>\n'
        '(?:          .*?\n)*'
        '        </externalReferences>',
        '        <vendor>CycloneDX</vendor>\n'
        '        <name>cyclonedx-python-lib</name>\n'
        '        <version>\\1</version>\n'
        '        <externalReferences><!-- stripped --></externalReferences>',
        bom)
    if sys.version_info < (3, 13):
        # py3.13 finally fixed a bug in the XML writer: https://github.com/python/cpython/issues/81555
        # no longer escape double-quotes(") in text/non-attribute.
        # here is a backwards-compat mode, so we have consistent tests.
        bom = re_sub(
            r'>[^<]*&quot;[^<]*<',
            lambda s: s[0].replace('&quot;', '"'),
            bom)
    return bom


def make_json_comparable(bom: str) -> str:
    bom = bom.replace(_root_file_uri_json, 'file://.../')
    bom = bom.replace(  # replace this version in metadata.tools.components[]
        f'          "name": {json_dumps(EXPECTED_TOOL_NAME)},\n'
        '          "type": "application",\n'
        f'          "version": {json_dumps(__this_version)}',
        f'          "name": {json_dumps(EXPECTED_TOOL_NAME)},\n'
        '          "type": "application",\n'
        '          "version": "thisVersion-testing"')
    bom = bom.replace(  # replace this version in metadata.tools[]
        f'        "name": {json_dumps(EXPECTED_TOOL_NAME)},\n'
        '        "vendor": "CycloneDX",\n'
        f'        "version": {json_dumps(__this_version)}',
        f'        "name": {json_dumps(EXPECTED_TOOL_NAME)},\n'
        '        "vendor": "CycloneDX",\n'
        '        "version": "thisVersion-testing"')
    bom = re_sub(  # replace lib-dynamics in metadata.tools.components[]
        '          "description": ".*?",\n'
        '          "externalReferences": \\[\n'
        '(?:            .*?\n)*'
        '          \\],\n'
        '          "group": "CycloneDX",\n'
        '          "licenses": \\[\n'
        '(?:            .*?\n)*'
        '          \\],\n'
        '          "name": "cyclonedx-python-lib",\n'
        '          "type": "library",\n'
        '          "version": ".*?"',
        '          "description": "stripped",\n'
        '          "externalReferences": [   ],\n'
        '          "group": "CycloneDX",\n'
        '          "licenses": [   ],\n'
        '          "name": "cyclonedx-python-lib",\n'
        '          "type": "library",\n'
        '          "version": "libVersion-testing"',
        bom)
    bom = re_sub(  # replace lib-dynamics version in metadata.tools[]
        '        "name": "cyclonedx-python-lib",\n'
        '        "vendor": "CycloneDX",\n'
        '        "version": ".*?"',
        '        "name": "cyclonedx-python-lib",\n'
        '        "vendor": "CycloneDX",\n'
        '        "version": "libVersion-testing"',
        bom)
    bom = re_sub(  # replace lib-dynamics externalReferences in metadata.tools[]
        '        "externalReferences": \\[\n'
        '(?:          .*?\n)*'
        '        \\],\n'
        '        "name": "cyclonedx-python-lib",\n'
        '        "vendor": "CycloneDX",\n',
        '        "externalReferences": [   ],\n'
        '        "name": "cyclonedx-python-lib",\n'
        '        "vendor": "CycloneDX",\n',
        bom)
    return bom


def make_comparable(bom: str, of: OutputFormat) -> str:
    if of is OutputFormat.XML:
        return make_xml_comparable(bom)
    if of is OutputFormat.JSON:
        return make_json_comparable(bom)
    raise NotImplementedError(f'unknown OutputFormat: {of!r}')

# endregion reproducible test results


def load_pyproject() -> Dict[str, Any]:
    if sys.version_info >= (3, 11):
        from tomllib import load as toml_load
    else:
        from tomli import load as toml_load
    with open(path.join(path.dirname(__file__), '..', 'pyproject.toml'), 'rb') as f:
        return toml_load(f)
