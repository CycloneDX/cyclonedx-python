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


from typing import TYPE_CHECKING, Any, BinaryIO

from . import BomBuilder

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model.bom import Bom


# !!! be as lazy loading as possible, as greedy as needed
# TODO: measure with `time -v` for max resident size and see if this changes when global imports are used


class RequirementsBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        from argparse import OPTIONAL, ArgumentParser, FileType
        from textwrap import dedent

        p = ArgumentParser(description='Build an SBOM from frozen requirements.',
                           epilog=dedent('''\
                           Example Usage:
                             • Build an SBOM from a frozen requirements file:
                                   $ %(prog)s requirements-prod.txt
                             • Merge multiple files and build an SBOM from it:
                                   $ cat requirements/*.txt | %(prog)s -
                             • Build an inventory for all installed packages:
                                   $ python3 -m pip freeze --all | %(prog)s -
                             • Build an inventory from an unfrozen manifest:
                                   $ python3 -m pip install -r dependencies.txt &&\\
                                     python3 -m pip freeze | %(prog)s -
                           '''),
                           **kwargs)
        p.add_argument('infile',
                       help='I HELP TODO (default: %(default)s)',
                       nargs=OPTIONAL,
                       type=FileType('rb'),
                       default='requirements.txt')
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 **kwargs: Any) -> None:
        self._logger = logger

    def __call__(self, *,  # type:ignore[override]
                 infile: BinaryIO,
                 **kwargs: Any) -> 'Bom':
        from collections import Counter

        from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, XsUri
        from cyclonedx.model.bom import Bom
        from cyclonedx.model.component import Component, ComponentType
        from packageurl import PackageURL
        from pip_requirements_parser import RequirementsFile

        from .utils.io import io2textfile

        bom = Bom()
        bom_refs = Counter()

        # no support for `include_nested` intended, so a temp file instead the original path is fine
        with io2textfile(infile) as ff:
            requirements = RequirementsFile.from_file(ff.name, include_nested=False).requirements
        for requirement in requirements:
            version = requirement.get_pinned_version or None
            download_url = requirement.link and requirement.link.url or None
            bom_ref = requirement.name or 'unknown'
            bom_refs[bom_ref] += 1
            if bom_refs[bom_ref] > 1:
                bom_ref += f'-{bom_refs[bom_ref]:x}'
            component = Component(
                type=ComponentType.LIBRARY,
                name=requirement.name or 'unknown',
                version=version,
                hashes=map(HashType.from_composite_str, requirement.hash_options),
                purl=PackageURL(type='pypi', name=requirement.name, version=version,
                                qualifiers=download_url and {'download_url': download_url}
                                ) if requirement.name else None,
                bom_ref=bom_ref,
                external_references=[
                    ExternalReference(type=ExternalReferenceType.DISTRIBUTION, url=XsUri(download_url))
                ] if download_url else None
            )

            self._logger.debug('Add component: %r', component)
            if not component.version:
                self._logger.warning('Component has no version: %r', component)
            bom.components.add(component)

        return bom
