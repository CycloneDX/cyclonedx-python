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

import sys
import argparse
import requirements
from cyclonedx import BomGenerator
from cyclonedx import BomValidator
from packaging.utils import canonicalize_version
from packaging.version import parse as packaging_parse


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


def _get_pypi_version(special_version, release_dict):
    """
    Loop over the pypi release dictionary looking for an equivalent version string. Return the alternative version
    if found, otherwise return None.
    :param special_version: The version string that failed to match against the Pypi versions.
    :param release_dict: Pypi's releases dictionary for a given module.
    :return: The matching version string or None if it not matched.
    """
    for release in release_dict:
        pypi_version = canonicalize_version(release)
        if special_version == pypi_version:
            return release
    return None


def read_bom(fd):
    """Read BOM data from file handle."""
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
                try:
                    version_release = releases[version]
                except KeyError as key_error:
                    parsed_version = packaging_parse(version)
                    if parsed_version.is_prerelease or parsed_version.is_postrelease or parsed_version.is_devrelease:
                        pypi_version = _get_pypi_version(version, releases)
                        if pypi_version:
                            version_release = releases[pypi_version]
                        else:
                            # Unable to find a matching normalized version string, re-throw exception
                            raise key_error
                    else:
                        # This wasn't one of the special case version strings we can handle, re-throw exception
                        raise key_error

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

    return component_elements


def main():
    parser = argparse.ArgumentParser(description='CycloneDX BOM Generator')
    parser.add_argument('-i', action="store", dest="input_file", default="requirements.txt")
    parser.add_argument('-o', action="store", dest="output_file", default="bom.xml")
    args = parser.parse_args()
    print("Input file: " + args.input_file)
    print("Output BOM: " + args.output_file)

    if args.input_file == '-':
        component_elements = read_bom(sys.stdin)
    else:
        with open(args.input_file, 'r') as fd:
            component_elements = read_bom(fd)

    # Generate the CycloneDX BOM and return it as an XML string
    bom_xml = BomGenerator.build_bom(component_elements)
    with open(args.output_file, "w") as text_file:
        text_file.write(bom_xml)

    print("Validating BOM")
    is_valid = BomValidator.is_valid(args.output_file)
    if is_valid:
        print("Complete")
    else:
        print("The generated BOM is not valid")

