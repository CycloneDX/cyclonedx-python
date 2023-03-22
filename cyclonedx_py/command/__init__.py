# encoding: utf-8
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
import functools
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Callable

import click
from click import Context
from click.decorators import FC
from cyclonedx.output import LATEST_SUPPORTED_SCHEMA_VERSION
from cyclonedx.schema.schema import SCHEMA_VERSIONS

from ..utils.output import CLI_OMITTABLE, CLI_OUTPUT_FORMAT

if sys.version_info >= (3, 8):
    from importlib.metadata import version as meta_version
else:
    from importlib_metadata import version as meta_version

cdx_version: str = 'TBC'
try:
    cdx_version = str(meta_version('cyclonedx-bom'))
except Exception:
    cdx_version = 'DEVELOPMENT'


class CycloneDxCmd:

    def __init__(self, *, warn_only: bool = False, debug: bool = False) -> None:
        self._warn_only = warn_only
        self._debug = debug

    @property
    def debug(self) -> bool:
        return self._debug

    @property
    def warn_only(self) -> bool:
        return self._warn_only


@click.group()
@click.option('-w', '--warn-only', is_flag=True, default=False, show_default=True, type=bool,
              help='Prevents exit with non-zero code when issues have been detected')
@click.option('-X', '--debug', is_flag=True, default=False, show_default=True, type=bool, help='Enable debug output')
@click.pass_context
def cli(ctx: Context, warn_only: bool, debug: bool) -> None:
    ctx.obj = CycloneDxCmd(warn_only=warn_only, debug=debug)

    if ctx.obj.debug:
        click.echo('*** DEBUG MODE ENABLED ***')


root_cdx_command = click.make_pass_decorator(CycloneDxCmd, ensure=True)


def input_python_options(f: FC) -> Callable[[FC], FC]:
    @click.option('-c', '--conda', 'input_type', flag_value='CONDA',
                  help='Build a SBOM based on the output from `conda list --explicit` or `conda list --explicit --md5`')
    @click.option('-cj', '--conda-json', 'input_type', flag_value='CONDA_JSON',
                  help='Build a SBOM based on the output from `conda list --json`')
    @click.option('-e', '--e', '--environment', 'input_type', default=True, flag_value='ENVIRONMENT',
                  help='Build a SBOM based on the packages installed in your current Python environment (DEFAULT)')
    @click.option('-p', '--p', '--poetry', 'input_type', flag_value='POETRY',
                  help='Build a SBOM based on a Poetry poetry.lock\'s contents. Use with -i to specify absolute path '
                       'to a `poetry.lock` you wish to use, else we\'ll look for one in the current working directory.')
    @click.option('-pip', '--pip', 'input_type', flag_value='PIPENV',
                  help='Build a SBOM based on a PipEnv Pipfile.lock\'s contents. Use with -i to specify absolute path '
                       'to a `Pipfile.lock` you wish to use, else we\'ll look for one in the current working '
                       'directory.')
    @click.option('-r', '--r', '--requirements', 'input_type', flag_value='REQUIREMENTS',
                  help='Build a SBOM based on a requirements.txt\'s contents. Use with -i to specify absolute path to '
                       'a `requirements.txt` you wish to use, else we\'ll look for one in the current working '
                       'directory.')
    @click.option('-i', '--in-file', type=click.File('r'),
                  help='File to read input from. Use "-" to read from STDIN.')
    @functools.wraps(f)
    def wrapper_common_options(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper_common_options


def output_cyclonedx_options(f: FC) -> Callable[[FC], FC]:
    @click.option('--format', 'output_format', type=click.Choice([f.value for f in CLI_OUTPUT_FORMAT]),
                  default=CLI_OUTPUT_FORMAT.XML.value,
                  help=f'The output format for your SBOM (default: {CLI_OUTPUT_FORMAT.XML.value})')
    @click.option('-F', '--force', is_flag=True, default=False,
                  help='If outputting to a file and the stated file already exists, it will be overwritten.')
    @click.option('-pb', '--purl-bom-ref', is_flag=True, default=False,
                  help='Use a component\'s PURL for the bom-ref value, instead of a random UUID')
    @click.option('-o', '--o', '--output', type=click.Path(), default='-',
                  help='Output file path for your SBOM. Use "-" to write to STDOUT.')
    @click.option('--omit', type=click.Choice([CLI_OMITTABLE.DevDependencies.value]),
                  help='Omit specified items when using Poetry or PipEnv')
    @click.option('--schema-version', 'schema_version', type=click.Choice(SCHEMA_VERSIONS.keys()),
                  default=LATEST_SUPPORTED_SCHEMA_VERSION.to_version(),
                  help=f'The CycloneDX schema version for your SBOM '
                       f'(default: {LATEST_SUPPORTED_SCHEMA_VERSION.to_version()})')
    @functools.wraps(f)
    def wrapper_common_options(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper_common_options


def _get_output_format(output_format: str) -> CLI_OUTPUT_FORMAT:
    return CLI_OUTPUT_FORMAT(str(output_format).lower())


class BaseCommand(ABC):

    def __init__(self, cmd: CycloneDxCmd) -> None:
        super().__init__()
        self.cmd = cmd

    def debug_message(self, message: str, *args: Any, **kwargs: Any) -> None:
        if self.cmd.debug:
            click.echo(f'[DEBUG] - {{__t}} - {message}'.format(*args, **kwargs, __t=datetime.now()), file=sys.stderr)

    @staticmethod
    def error_and_exit(message: str, *args: Any, exit_code: int = 1, **kwargs: Any) -> int:
        click.echo(f'[ERROR] - {{__t}} - {message}'.format(*args, **kwargs, __t=datetime.now()), file=sys.stderr)
        return exit_code

    @abstractmethod
    def execute(self) -> int:
        pass
