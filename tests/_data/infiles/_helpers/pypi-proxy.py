#!/usr/bin/env python3

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

"""
This is a small http proxy to PyPI.
This might be needed to play certain setups.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from os import unlink
from sys import argv, stderr
from urllib.request import urlretrieve


class PypiProxyReqHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa:N802
        print('PyPI-PROXY > ', self.path, file=stderr)
        p, m = urlretrieve(f'https://pypi.org{self.path}')  # nosec B310
        print('PyPI-PROXY < ', p, file=stderr)
        self.send_response(200)
        for k, v in m.items():
            self.send_header(k, v)
        self.end_headers()
        with open(p, 'rb') as f:
            self.wfile.write(f.read())
        unlink(p)


def make_proxy(port: int) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(
        ('127.0.0.1', port),
        PypiProxyReqHandler)


if __name__ == '__main__':
    proxy = make_proxy(int(argv[1]) if len(argv) >= 2 else 8080)
    print(f'running PyPI proxy at: {proxy.server_address!r}', file=stderr)
    try:
        proxy.serve_forever()
    except KeyboardInterrupt:
        proxy.server_close()
