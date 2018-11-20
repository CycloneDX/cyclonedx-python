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

def populate_digests(hashes, digests):
    for sig in digests:
        if sig == "md5":
            hashes["MD5"] = digests[sig]
        elif sig == "sha1":
            hashes["SHA-1"] = digests[sig]
        elif sig == "sha256":
            hashes["SHA-256"] = digests[sig]
        elif sig == "sha512":
            hashes["SHA-512"] = digests[sig]


def main():
    parser = argparse.ArgumentParser(description='CycloneDX BOM Generator')
    parser.add_argument('-i', action="store", dest="input_file", default="requirements.txt")
    parser.add_argument('-o', action="store", dest="output_file", default="bom.xml")
    args = parser.parse_args()
    print("Input file: " + args.input_file)
    print("Output BOM: " + args.output_file)

    with open(args.input_file, 'r') as fd:
        print("Generating CycloneDX BOM")
        component_elements = []
        for req in requirements.parse(fd):
            name = req.name
            if not req.specs:
                print("WARNING: " + name + " does not have a version specified. Skipping.")
                break

            if len(req.specs[0]) >= 2:
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

                    # This should be optimized a bit - kinda ugly
                    hashes = {}
                    releases = json["releases"]
                    version_release = releases[version]
                    has_wheel = False
                    for release in version_release:
                        if release["packagetype"] == "bdist_wheel":
                            has_wheel = True
                    # pip will always prefer bdist_wheel over sdist - therefore hashes from bdist_wheel take precedence
                    for release in version_release:
                        if has_wheel is True and release["packagetype"] == "bdist_wheel":
                            populate_digests(hashes, release["digests"])
                        elif has_wheel is False and release["packagetype"] == "sdist":
                            populate_digests(hashes, release["digests"])

                    purl = BomGenerator.generate_purl(name, version)
                    component = BomGenerator.build_component_element(author, name, version, description, hashes, license, purl, "false")
                    component_elements.append(component)
                else:
                    # nothing to parse, simply add the name, version, and purl to bom
                    purl = BomGenerator.generate_purl(name, version)
                    component = BomGenerator.build_component_element("", name, version, "", {}, "", purl, "false")
                    component_elements.append(component)

    # Generate the CycloneDX BOM and return it as an XML string
    bom_xml = BomGenerator.build_bom(component_elements)
    text_file = open(args.output_file, "w")
    text_file.write(bom_xml)
    text_file.close()

    print("Validating BOM")
    is_valid = BomValidator.is_valid(args.output_file)
    if is_valid:
        print("Complete")
    else:
        print("The generated BOM is not valid")
