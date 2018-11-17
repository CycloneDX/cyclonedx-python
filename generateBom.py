#!/usr/bin/env python
# encoding: utf-8

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

import argparse
import requirements
from cyclonedx import BomGenerator
from cyclonedx import BomValidator


parser = argparse.ArgumentParser(description='CycloneDX BOM Generator')
parser.add_argument('-i', action="store", dest="input_file", default="requirements.txt")
parser.add_argument('-o', action="store", dest="output_file", default="bom.xml")
args = parser.parse_args()
print("Input file: " + args.input_file)
print("Output BOM: " + args.output_file)


def main(requirementsFile, bomOutputFile):
    with open(requirementsFile, 'r') as fd:
        print("Generating CycloneDX BOM")
        component_elements = []
        for req in requirements.parse(fd):
            if len(req.specs[0]) >= 2:
                name = req.name
                version = req.specs[0][1]
                if req.specs[0][0] != "==":
                    print("WARNING: " + name + " is not pinned to a specific version. Using: " + version)
                response = BomGenerator.get_package_info(name, version)
                if response:
                    json = response.json()
                    info = json["info"]
                    author = info["author"]
                    description = info["summary"]
                    license = info["license"]  # TODO: Attempt to perform SPDX license ID resolution
                    purl = BomGenerator.generate_purl(name, version)
                    component = BomGenerator.build_component_element(author, name, version, description, license, purl, "false")
                    component_elements.append(component)
                else:
                    # nothing to parse, simply add the name, version, and purl to bom
                    purl = BomGenerator.generate_purl(name, version)
                    component = BomGenerator.build_component_element("", name, version, "", "", purl, "false")
                    component_elements.append(component)

    # Generate the CycloneDX BOM and return it as an XML string
    bom_xml = BomGenerator.build_bom(component_elements)
    text_file = open(bomOutputFile, "w")
    text_file.write(bom_xml)
    text_file.close()

    print("Validating BOM")
    is_valid = BomValidator.is_valid(bomOutputFile)
    if is_valid:
        print("Complete")
    else:
        print("The generated BOM is not valid")


main(args.input_file, args.output_file)
