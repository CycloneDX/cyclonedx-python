# This file is part of CycloneDX Python module.
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
# Copyright (c) Steve Springett. All Rights Reserved.

import os
import json
import jsonschema
import xmlschema

xml_bom_schema_path = os.path.join(os.path.dirname(__file__), "../schema/bom-1.0.xsd")
xml_bom_schema = xmlschema.XMLSchema(xml_bom_schema_path)
json_bom_schema_path = os.path.join(os.path.dirname(__file__), "../schema/bom-1.2.schema.json")
with open(json_bom_schema_path, 'rt') as f:
    json_bom_schema = json.load(f)

def is_valid(output_filename, is_json):
    if is_json:
        try:
            with open(output_filename, 'rt') as f:
                bom_contents = json.load(f)
            jsonschema.validate(bom_contents, json_bom_schema)
            return True
        except jsonschema.ValidationError as e:
            print(e)
            return False
    else:
        return xml_bom_schema.is_valid(output_filename)
