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

"""The following structures are internal helpers."""

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from mypy_extensions import Arg, KwArg, VarArg

    DebugMessageCallback = Callable[[Arg(str, 'message'), VarArg(Any), KwArg(Any)], None]  # noqa: F821
    """Callback for debug messaging.

    :parameter message: the format string.
    :Other Parameters: the *args: to :func:`str.forma()`.
    :Keyword Arguments: the **kwargs to :func:`str.format()`.
    """
else:
    DebugMessageCallback = Callable[..., None]


def quiet(message: str, *_: Any, **__: Any) -> None:
    """Do not print anything.

     Must be compatible to :py:data:`DebugMessageCallback`.
     """
    pass
