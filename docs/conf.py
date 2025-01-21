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

# -- Project information -----------------------------------------------------

from datetime import date

project = 'CycloneDX Python'
copyright = f'{date.today().strftime("%Y")}, Copyright (c) OWASP Foundation'
author = 'Jan Kowalleck, Paul Horton, Steve Springett, Patrick Dwyer'

# The full version, including alpha/beta/rc tags
# !! version is managed by semantic_release
release = "5.1.2"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    # "sphinx.ext.viewcode",
    # "autoapi.extension",
    "sphinx_rtd_theme",
    "m2r2"
]

# Document Python Code
# autoapi_type = 'python'
# autoapi_dirs = ['../cyclonedx_py']
# see https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_options
# autoapi_options = ['show-module-summary', 'members', 'undoc-members', 'inherited-members', 'show-inheritance']

source_suffix = ['.rst', '.md']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# see https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-exclude_patterns
exclude_patterns = [
    'processes',  # internal docs
    '_build',  # build target
    '.*', '**/.*',  # dotfiles and folders
    'Thumbs.db', '**/Thumbs.db',
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
