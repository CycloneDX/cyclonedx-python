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
from pkg_resources import Distribution

if sys.version_info >= (3, 8):
    if sys.version_info >= (3, 10):
        from importlib.metadata import PackageMetadata as _MetadataReturn
    else:
        from email.message import Message as _MetadataReturn
    from importlib.metadata import metadata
else:
    from importlib_metadata import metadata, PackageMetadata as _MetadataReturn

from cyclonedx.factory.license import LicenseChoiceFactory, LicenseFactory
from cyclonedx.model.component import Component
from cyclonedx.parser import BaseParser

from .._internal.trove_classifier_license import (
    TROVE_CLASSIFIER_PREFIX_LICENSE as _TC_PREFIX_LICENSE,
    trove_classifier_license_clean as _tc_license_clean,
    trove_classifier_license_to_spdx_id as _tc_license2spdx,
)
from ._debug import DebugMessageCallback, quiet


class EnvironmentParser(BaseParser):
    """
    This will look at the current Python environment and list out all installed packages.

    Best used when you have virtual Python environments per project.
    """

    def __init__(
            self, use_purl_bom_ref: bool = False,
            *,
            debug_message: DebugMessageCallback = quiet
    ) -> None:
        super().__init__()
        debug_message('init {}', self.__class__.__name__)

        debug_message('late import pkg_resources')
        import pkg_resources

        lcfac = LicenseChoiceFactory(license_factory=LicenseFactory())

        debug_message('processing pkg_resources.working_set')
        i: Distribution
        for i in iter(pkg_resources.working_set):
            debug_message('processing working_set item: {!r}', i)
            purl = PackageURL(type='pypi', name=i.project_name, version=i.version)
            bom_ref = purl.to_string() if use_purl_bom_ref else None
            c = Component(name=i.project_name, bom_ref=bom_ref, version=i.version, purl=purl)

            i_metadata = self._get_metadata_for_package(i.project_name)
            debug_message('processing i_metadata')
            if 'Author' in i_metadata:
                debug_message('processing i_metadata Author: {!r}', i_metadata['Author'])
                c.author = i_metadata['Author']
            if 'License' in i_metadata and i_metadata['License'] and i_metadata['License'] != 'UNKNOWN':
                debug_message('processing i_metadata License: {!r}', i_metadata['License'])
                try:
                    c.licenses.add(lcfac.make_from_string(i_metadata['License']))
                except CycloneDxModelException as error:
                    # @todo traceback and details to the output?
                    debug_message('Warning: suppressed {!r}', error)
                    del error

            debug_message('processing classifiers')
            for classifier in i_metadata.get_all("Classifier", []):
                debug_message('processing classifier: {!r}', classifier)
                classifier = str(classifier).strip()
                if classifier.startswith(_TC_PREFIX_LICENSE):
                    license_string = _tc_license2spdx(classifier) or _tc_license_clean(classifier)
                    try:
                        c.licenses.add(lcfac.make_from_string(license_string))
                    except CycloneDxModelException as error:
                        # @todo traceback and details to the output?
                        debug_message('Warning: suppressed {!r}', error)
                        del error

            self._components.append(c)

    @staticmethod
    def _get_metadata_for_package(package_name: str) -> _MetadataReturn:
        return metadata(package_name)
