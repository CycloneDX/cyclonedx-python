# encoding: utf-8

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

"""
Parser classes for reading installed packages in your current Python environment.

These parsers look at installed packages only - not what you have defined in any dependency tool - see the other Parsers
if you want to derive CycloneDX from declared dependencies.


The Environment Parsers support population of the following data about Components:

"""

import sys

from cyclonedx.exception.model import CycloneDxModelException

# See https://github.com/package-url/packageurl-python/issues/65
from packageurl import PackageURL  # type: ignore
from pkg_resources import DistInfoDistribution  # type: ignore

if sys.version_info >= (3, 8):
    if sys.version_info >= (3, 10):
        from importlib.metadata import PackageMetadata as _MetadataReturn
    else:
        from email.message import Message as _MetadataReturn
    from importlib.metadata import metadata
else:
    from importlib_metadata import metadata, PackageMetadata as _MetadataReturn

from cyclonedx.model import License, LicenseChoice
from cyclonedx.model.component import Component
from cyclonedx.parser import BaseParser


class EnvironmentParser(BaseParser):
    """
    This will look at the current Python environment and list out all installed packages.

    Best used when you have virtual Python environments per project.
    """

    def __init__(self, use_purl_bom_ref: bool = False) -> None:
        super().__init__()

        import pkg_resources

        i: DistInfoDistribution
        for i in iter(pkg_resources.working_set):
            purl = PackageURL(type='pypi', name=i.project_name, version=i.version)
            bom_ref = purl.to_string() if use_purl_bom_ref else None
            c = Component(name=i.project_name, bom_ref=bom_ref, version=i.version, purl=purl)

            i_metadata = self._get_metadata_for_package(i.project_name)
            if 'Author' in i_metadata:
                c.author = i_metadata['Author']

            if 'License' in i_metadata and i_metadata['License'] and i_metadata['License'] != 'UNKNOWN':
                # Values might be ala `MIT` (SPDX id), `Apache-2.0 license` (arbitrary string), ...
                # Therefore, just go with a named license.
                try:
                    c.licenses.add(LicenseChoice(license_=License(license_name=i_metadata['License'])))
                except CycloneDxModelException:
                    # write a debug message?
                    pass

            for classifier in i_metadata.get_all("Classifier", []):
                # Trove classifiers - https://packaging.python.org/specifications/core-metadata/#metadata-classifier
                # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
                if str(classifier).startswith('License :: OSI Approved :: '):
                    license_name = str(classifier).replace('License :: OSI Approved :: ', '').strip()
                elif str(classifier).startswith('License :: '):
                    license_name = str(classifier).replace('License :: ', '').strip()
                else:
                    license_name = ''
                if license_name:
                    try:
                        c.licenses.add(LicenseChoice(license_=License(license_name=license_name)))
                    except CycloneDxModelException:
                        # write a debug message?
                        pass

            self._components.append(c)

    @staticmethod
    def _get_metadata_for_package(package_name: str) -> _MetadataReturn:
        return metadata(package_name)
