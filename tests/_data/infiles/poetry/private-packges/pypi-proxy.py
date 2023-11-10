#!/usr/bin/env python3

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
This is a small http proxy to PiPI.
This might be needed to play this setup.
"""

import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from os import unlink
from urllib.request import urlretrieve


class PypiProxyReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('> ', self.path, file=sys.stderr)
        p, m = urlretrieve(f'https://pypi.org{self.path}')
        print('< ', p, file=sys.stderr)
        self.send_response(200)
        for k, v in m.items():
            self.send_header(k, v)
        self.end_headers()
        with open(p, 'rb') as f:
            self.wfile.write(f.read())
        unlink(p)


if __name__ == '__main__':
    server_address = ('', int(sys.argv[1]) if len(sys.argv) >= 2 else 8080)
    httpd = ThreadingHTTPServer(server_address, PypiProxyReqHandler)
    print(f'running PyPI proxy at: {server_address!r}', file=sys.stderr)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
