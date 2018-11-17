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

import requests
from xml.etree import ElementTree
from packageurl import PackageURL


def get_package_info(package_name, package_version):
    ship_api_url = "https://pypi.org/pypi/" + package_name + "/" + package_version + "/json"
    request_data = requests.get(ship_api_url)
    return request_data


def generate_purl(package_name, package_version):
    return PackageURL("pypi", '', package_name, package_version, '', '').to_string()


def build_bom(component_elements):
    declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    namespace = {'xmlns': 'http://cyclonedx.org/schema/bom/1.0', 'version': '1'}
    bom = ElementTree.Element("bom", namespace)
    components = ElementTree.Element("components")
    for component in component_elements:
        components.append(component)
    bom.append(components)
    return declaration + ElementTree.tostring(bom).decode()


def build_component_element(publisher, name, version, description, hashes, license, purl, modified):
    component = ElementTree.Element("component", {"type": "library"})
    if publisher and publisher != 'UNKNOWN':
        elm = ElementTree.Element("publisher")
        elm.text = publisher
        component.append(elm)
    if name and name != "UNKNOWN":
        elm = ElementTree.Element("name")
        elm.text = name
        component.append(elm)
    if version and version != "UNKNOWN":
        elm = ElementTree.Element("version")
        elm.text = version
        component.append(elm)
    if description and description != "UNKNOWN":
        elm = ElementTree.Element("description")
        elm.text = description
        component.append(elm)
    if len(hashes) > 0:
        hashes_elm = ElementTree.Element("hashes")
        for h in hashes:
            elm = ElementTree.Element("hash", {"alg": h})
            elm.text = hashes[h]
            hashes_elm.append(elm)
        component.append(hashes_elm)
    if license and license != "UNKNOWN":
        licenses_elm = ElementTree.Element("licenses")
        license_elm = ElementTree.Element("license")
        name_elm = ElementTree.Element("name")
        name_elm.text = license
        license_elm.append(name_elm)
        licenses_elm.append(license_elm)
        component.append(licenses_elm)
    if purl:
        elm = ElementTree.Element("purl")
        elm.text = purl
        component.append(elm)
    if modified:
        elm = ElementTree.Element("modified")
        elm.text = modified
        component.append(elm)
    else:
        elm = ElementTree.Element("modified")
        elm.text = "false"
        component.append(elm)
    return component
