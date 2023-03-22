#!/usr/bin/env python
# encoding: utf-8

# This file is part of CycloneDX Python
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
from .command import cli, cdx_version
from .command.make_bom import make_bom

_SUPPORTED_COMMANDS = [make_bom]


@cli.command(help='Show which version of CycloneDX BOM Generator you are running')
def version() -> None:
    print(f'You are running CycloneDX Python BOM Generator version {cdx_version}')


if __name__ == "__main__":
    cli()
