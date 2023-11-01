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


from os import unlink
from typing import TYPE_CHECKING, Any, BinaryIO, Iterable

from . import BomBuilder

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model.bom import Bom
    from pip_requirements_parser import InstallRequirement


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
        from pip_requirements_parser import RequirementsFile  # type: ignore[import-untyped]

        from .utils.io import io2textfile

        # no support for `include_nested` intended, so a temp file instead the original path is fine
        rf = io2textfile(infile)
        try:
            return self._make_bom(
                RequirementsFile.from_file(rf, include_nested=False).requirements
            )
        finally:
            unlink(rf)

    def _make_bom(self, requirements: Iterable['InstallRequirement']) -> 'Bom':
        from cyclonedx.exception.model import InvalidUriException
        from cyclonedx.model import ExternalReference, ExternalReferenceType, HashType, XsUri
        from cyclonedx.model.component import Component, ComponentType
        from packageurl import PackageURL

        from .utils.bom import make_bom

        bom = make_bom()

        for requirement in requirements:
            name = requirement.name
            version = requirement.get_pinned_version or None
            external_references = []
            purl_qualifiers = {}  # see https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst

            # workaround for https://github.com/nexB/pip-requirements-parser/issues/24
            is_local = requirement.is_local_path and (not requirement.link or requirement.link.scheme in ['', 'file'])
            if is_local:
                if requirement.is_wheel or requirement.is_archive:
                    purl_qualifiers['file_name'] = requirement.link.url
                    try:
                        external_references.append(ExternalReference(
                            comment='local path to wheel/archive',
                            type=ExternalReferenceType.OTHER,
                            url=XsUri(requirement.link.url)))
                    except InvalidUriException:
                        pass  # safe to pass, as the actual line is documented as `description`
            elif requirement.is_url:
                if 'pythonhosted.org/' not in requirement.link.url:
                    # skip PURL bloat, do not add implicit information
                    purl_qualifiers['vcs_url' if requirement.is_vcs_url else 'download_url'] = requirement.link.url
                try:
                    external_references.append(ExternalReference(
                        type=ExternalReferenceType.VCS if requirement.is_vcs_url else ExternalReferenceType.DISTRIBUTION,
                        url=XsUri(requirement.link.url)))
                except InvalidUriException:
                    pass  # safe to pass, as the actual line is documented as `description`

            component = Component(
                bom_ref=f'requirements-L{requirement.line_number}',
                description=f'requirements line {requirement.line_number}: {requirement.line}',
                type=ComponentType.LIBRARY,
                name=name or 'unknown',
                version=version,
                hashes=map(HashType.from_composite_str, requirement.hash_options),
                purl=PackageURL(type='pypi', name=requirement.name, version=version,
                                qualifiers=purl_qualifiers
                                ) if not is_local and name else None,
                external_references=external_references,
            )

            self._logger.debug('Add component: %r', component)
            if not component.version:
                self._logger.warning('Component has no version: %r', component)
            bom.components.add(component)

        return bom
