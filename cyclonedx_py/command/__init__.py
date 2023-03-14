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

import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from datetime import datetime
from typing import Any, Optional

if sys.version_info >= (3, 8):
    from importlib.metadata import version as meta_version
else:
    from importlib_metadata import version as meta_version

cdx_version: str = 'TBC'
try:
    cdx_version = str(meta_version('cyclonedx-bom'))  # type: ignore[no-untyped-call]
except Exception:
    cdx_version = 'DEVELOPMENT'


class BaseCommand(ABC):

    def __init__(self, debug_enabled: bool = False) -> None:
        super().__init__()
        self._debug_enabled = debug_enabled
        self._arguments: Optional[Namespace] = None

        self._debug_message('!!! DEBUG MODE ENABLED !!!')
        self._debug_message('Parsed Arguments: {}', self._arguments)

    @property
    def debug_enabled(self) -> bool:
        return self._debug_enabled

    def execute(self, arguments: Namespace) -> int:
        self._arguments = arguments
        return self.handle_args()

    @abstractmethod
    def handle_args(self) -> int:
        pass

    @abstractmethod
    def get_argument_parser_name(self) -> str:
        pass

    @abstractmethod
    def get_argument_parser_help(self) -> str:
        pass

    @abstractmethod
    def setup_argument_parser(self, arg_parser: ArgumentParser) -> None:
        pass

    @property
    def arguments(self) -> Namespace:
        if self._arguments:
            return self._arguments

        raise ValueError('Arguments have not been set yet - execute() has to be called first')

    def _debug_message(self, message: str, *args: Any, **kwargs: Any) -> None:
        if self.debug_enabled:
            print(f'[DEBUG] - {{__t}} - {message}'.format(*args, **kwargs, __t=datetime.now()),
                  file=sys.stderr)

    @staticmethod
    def _error_and_exit(message: str, *args: Any, exit_code: int = 1, **kwargs: Any) -> int:
        print(f'[ERROR] - {{__t}} - {message}'.format(*args, **kwargs, __t=datetime.now()),
              file=sys.stderr)
        return exit_code
