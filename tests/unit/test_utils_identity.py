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


from decimal import Decimal
from json import loads as json_loads
from unittest import TestCase
from xml.etree.ElementTree import fromstring as xml_fromstring  # nosec:B405

from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.component_evidence import AnalysisTechnique, IdentityField
from cyclonedx.output import make_outputter
from cyclonedx.schema import OutputFormat, SchemaVersion
from cyclonedx.validation import make_schemabased_validator

from cyclonedx_py._internal.utils.identity import make_identity_evidence


class TestIdentityEvidence(TestCase):
    def test_records_declared_values_and_source(self) -> None:
        evidence = make_identity_evidence(name='Some_Package', version='01.0+local', source='poetry.lock')
        self.assertIsNotNone(evidence)
        identities = {identity.field: identity for identity in evidence.identity}
        self.assertEqual({IdentityField.NAME, IdentityField.VERSION}, set(identities))
        for field, value in ((IdentityField.NAME, 'Some_Package'), (IdentityField.VERSION, '01.0+local')):
            with self.subTest(field=field):
                identity = identities[field]
                self.assertEqual(value, identity.concluded_value)
                self.assertIsNone(identity.confidence)
                self.assertFalse(identity.tools)
                self.assertEqual(1, len(identity.methods))
                method = next(iter(identity.methods))
                self.assertIs(AnalysisTechnique.MANIFEST_ANALYSIS, method.technique)
                self.assertEqual(Decimal(1), method.confidence)
                self.assertEqual('poetry.lock', method.value)

    def test_omits_missing_fields(self) -> None:
        for name, version, expected_field in (
            ('package', None, IdentityField.NAME),
            ('package', '', IdentityField.NAME),
            (None, '1.0', IdentityField.VERSION),
            ('', '1.0', IdentityField.VERSION),
        ):
            with self.subTest(name=name, version=version):
                evidence = make_identity_evidence(name=name, version=version, source='package metadata')
                self.assertIsNotNone(evidence)
                self.assertEqual([expected_field], [identity.field for identity in evidence.identity])

    def test_no_evidence_without_values(self) -> None:
        for name, version in ((None, None), ('', ''), (None, ''), ('', None)):
            with self.subTest(name=name, version=version):
                self.assertIsNone(make_identity_evidence(name=name, version=version, source='package metadata'))

    def test_schema_serialization(self) -> None:
        component = Component(
            name='example', version='1.0', type=ComponentType.LIBRARY,
            evidence=make_identity_evidence(name='example', version='1.0', source='poetry.lock'),
        )
        schemas = (schema for schema in SchemaVersion
                   if tuple(map(int, schema.to_version().split('.'))) >= (1, 4))
        for schema in schemas:
            for output_format in (OutputFormat.JSON, OutputFormat.XML):
                with self.subTest(schema=schema, output_format=output_format):
                    outputter = make_outputter(
                        bom=Bom(components=[component]), output_format=output_format, schema_version=schema,
                    )
                    if schema is SchemaVersion.V1_5:
                        with self.assertWarnsRegex(UserWarning, 'does not support multiple identity items'):
                            output = outputter.output_as_string()
                    else:
                        output = outputter.output_as_string()
                    self.assertFalse(make_schemabased_validator(output_format, schema).validate_str(output))
                    expected_fields = [] if schema is SchemaVersion.V1_4 else (
                        ['name'] if schema is SchemaVersion.V1_5 else ['name', 'version'])
                    if output_format is OutputFormat.JSON:
                        raw = json_loads(output)['components'][0].get('evidence', {}).get('identity', [])
                        identities = [raw] if isinstance(raw, dict) else raw
                        self.assertEqual(expected_fields, [identity['field'] for identity in identities])
                        for identity in identities:
                            if schema is SchemaVersion.V1_5:
                                self.assertNotIn('concludedValue', identity)
                            else:
                                self.assertEqual({'name': 'example', 'version': '1.0'}[identity['field']],
                                                 identity['concludedValue'])
                            self.assertEqual([{'technique': 'manifest-analysis', 'confidence': 1,
                                               'value': 'poetry.lock'}], identity['methods'])
                    else:
                        # Only parse the XML generated above from a fixed in-memory component.
                        identities = xml_fromstring(output).findall('.//{*}identity')  # nosec:B314
                        self.assertEqual(expected_fields, [identity.findtext('{*}field') for identity in identities])
                        for identity in identities:
                            concluded = identity.findtext('{*}concludedValue')
                            if schema is SchemaVersion.V1_5:
                                self.assertIsNone(concluded)
                            else:
                                self.assertEqual({'name': 'example', 'version': '1.0'}[
                                    identity.findtext('{*}field')], concluded)
                            methods = identity.findall('{*}methods/{*}method')
                            self.assertEqual(1, len(methods))
                            self.assertEqual('manifest-analysis', methods[0].findtext('{*}technique'))
                            self.assertEqual('poetry.lock', methods[0].findtext('{*}value'))
