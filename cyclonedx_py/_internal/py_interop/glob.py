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

__all__ = ['glob']

import sys
from glob import glob as _glob

if sys.version_info >= (3, 10):
    glob = _glob
else:
    from os.path import join, sep
    from typing import Optional

    def glob(pathname: str, *, root_dir: Optional[str] = None, recursive: bool = False) -> list[str]:
        if root_dir is not None:
            pathname = join(root_dir, pathname)
        files = _glob(pathname, recursive=recursive)
        if root_dir is not None:
            if not root_dir.endswith(sep):
                root_dir += sep
            files = [f.removeprefix(root_dir) for f in files]
        return files
