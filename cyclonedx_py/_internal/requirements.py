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


from typing import TYPE_CHECKING, Any, Generator, List, Set

from . import BomBuilder

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from logging import Logger

    from cyclonedx.model import HashType
    from cyclonedx.model.bom import Bom
    from cyclonedx.model.component import Component
    from pip_requirements_parser import InstallRequirement, RequirementsFile  # type:ignore[import-untyped]


# !!! be as lazy loading as possible, as greedy as needed
# TODO: measure with `/bin/time -v` for max resident size and see if this changes when global imports are used


class RequirementsBB(BomBuilder):

    @staticmethod
    def make_argument_parser(**kwargs: Any) -> 'ArgumentParser':
        from argparse import OPTIONAL, ArgumentParser
        from textwrap import dedent

        p = ArgumentParser(description=dedent(""""\
                           Build an SBOM from Pip requirements.

                           The options mimic the respective ones from Pip.
                           """),
                           epilog=dedent("""\
                           Example Usage:
                             • Build an SBOM from a requirements file:
                                   $ %(prog)s requirements-prod.txt
                             • Merge multiple files and build an SBOM from it:
                                   $ cat requirements/*.txt | %(prog)s -
                             • Build an inventory for all installed packages:
                                   $ python3 -m pip freeze --all | %(prog)s -
                             • Build an inventory from an unfrozen manifest:
                                   $ python3 -m pip install -r dependencies.txt &&\\
                                     python3 -m pip freeze | %(prog)s -
                           """),
                           **kwargs)
        # the args shall mimic the ones from Pip
        p.add_argument('-i', '--index-url',
                       metavar='URL',
                       help='Base URL of the Python Package Index'
                            ' (default: %(default)s) '
                            ' This should point to a repository compliant with PEP 503 (the simple repository API)'
                            ' or a local directory laid out in the same format.',
                       dest='index_url',
                       default='https://pypi.org/simple')
        p.add_argument('--extra-index-url',
                       metavar='URL',
                       help='Extra URLs of package indexes to use in addition to --index-url.'
                            ' Should follow the same rules as --index-url',
                       action='append',
                       dest='extra_index_urls',
                       default=[])
        p.add_argument('requirements_file',
                       metavar='requirements-file',
                       help='I HELP TODO (default: %(default)r in current working directory)',
                       nargs=OPTIONAL,
                       default='requirements.txt')
        return p

    def __init__(self, *,
                 logger: 'Logger',
                 index_url: str,
                 extra_index_urls: List[str],
                 **kwargs: Any) -> None:
        self._logger = logger
        self._index_url = index_url
        self._extra_index_urls = set(extra_index_urls)

    def __call__(self, *,  # type:ignore[override]
                 requirements_file: str,
                 **kwargs: Any) -> 'Bom':
        from os import unlink

        from pip_requirements_parser import RequirementsFile

        if requirements_file == '-':
            from sys import stdin

            from .utils.io import io2file

            rt = io2file(stdin.buffer)
            try:
                rf = RequirementsFile.from_file(rt, include_nested=False)
            finally:
                unlink(rt)
        else:
            rf = RequirementsFile.from_file(requirements_file, include_nested=True)

        return self._make_bom(rf)

    def _make_bom(self, rf: 'RequirementsFile') -> 'Bom':
        from functools import reduce

        from .utils.bom import make_bom

        bom = make_bom()

        index_url = reduce(lambda c, i: i.options.get('index_url') or c, rf.options, self._index_url)
        extra_index_urls = self._extra_index_urls.union(*(
            i.options['extra_index_urls'] for i in rf.options if 'extra_index_urls' in i.options))
        self._logger.debug('index_url = %r', index_url)
        self._logger.debug('extra_index_urls = %r', extra_index_urls)

        for requirement in rf.requirements:
            component = self._make_component(requirement, index_url, extra_index_urls)
            self._logger.debug('Add component: %r', component)
            if not component.version:
                self._logger.warning('Component has no pinned version: %r', component)
            bom.components.add(component)

        return bom

    def __hashes4req(self, req: 'InstallRequirement') -> Generator['HashType', None, None]:
        from cyclonedx.exception.model import UnknownHashTypeException
        from cyclonedx.model import HashType

        for hash in req.hash_options:
            try:
                yield HashType.from_composite_str(hash)
            except UnknownHashTypeException as error:
                self._logger.debug('skipping hash %s', hash, exc_info=error)
                del error

    def _make_component(self, req: 'InstallRequirement',
                        index_url: str, extra_index_urls: Set[str]) -> 'Component':
        from cyclonedx.exception.model import InvalidUriException
        from cyclonedx.model import ExternalReference, ExternalReferenceType, Property, XsUri
        from cyclonedx.model.component import Component, ComponentType
        from packageurl import PackageURL

        from . import PropertyName

        name = req.name
        version = req.get_pinned_version or None
        hashes = list(self.__hashes4req(req))
        external_references = []
        purl_qualifiers = {}  # see https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst

        # workaround for https://github.com/nexB/pip-requirements-parser/issues/24
        is_local = req.is_local_path and (not req.link or req.link.scheme in ['', 'file'])
        try:
            if is_local:
                external_references.append(ExternalReference(
                    comment='explicit local path',
                    type=ExternalReferenceType.OTHER,
                    url=XsUri(req.link.url),
                    hashes=hashes))
            elif req.is_url:
                if '://files.pythonhosted.org/' not in req.link.url:
                    # skip PURL bloat, do not add implicit information
                    purl_qualifiers['vcs_url' if req.is_vcs_url else 'download_url'] = req.link.url
                external_references.append(ExternalReference(
                    comment='explicit dist url',
                    type=ExternalReferenceType.VCS if req.is_vcs_url else ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(req.link.url),
                    hashes=hashes))
            else:
                # url based on https://warehouse.pypa.io/api-reference/legacy.html
                external_references.append(ExternalReference(
                    comment='implicit dist url',
                    type=ExternalReferenceType.DISTRIBUTION,
                    url=XsUri(f'{index_url or self._index_url}/{name}/'),
                    hashes=hashes))
                for eiurl in extra_index_urls:
                    external_references.append(ExternalReference(
                        comment='implicit dist extra-url',
                        type=ExternalReferenceType.DISTRIBUTION,
                        url=XsUri(f'{eiurl}/{name}/'),
                        hashes=hashes))
        except InvalidUriException as error:
            self._logger.debug('failed ExternalReference/url URL for: %s', req.line, exc_info=error)
            del error

        return Component(
            bom_ref=f'requirements-L{req.line_number}',
            description=f'requirements line {req.line_number}: {req.line}',
            type=ComponentType.LIBRARY,
            name=name or 'unknown',
            version=version,
            purl=PackageURL(type='pypi', name=req.name, version=version,
                            qualifiers=purl_qualifiers
                            ) if not is_local and name else None,
            external_references=external_references,
            properties=(Property(
                name=PropertyName.PackageExtra.value,
                value=extra
            ) for extra in req.extras)
        )
