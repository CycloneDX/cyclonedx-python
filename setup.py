#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cyclonedx-bom',
    version='0.1.0',
    description='CycloneDX bill-of-material (BOM) generation utility',
    long_description=long_description,
    long_description_content_type="text/markdown",
    # packages=['cyclonedx', 'cyclonedx.schema'],
    packages=setuptools.find_packages(),
    package_data={'cyclonedx.schema': ['bom-1.0.xsd', 'spdx.xsd']},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requirements',
        'packageurl',
        'xml.etree',
    ],
    entry_points={  # Links 'hello1234' command with a function to call
        'console_scripts': ['cyclonedx-py=generateBom:main']
    },
    author='Steve Springett',
    author_email='steve.springett@owasp.org',
    maintainer='Steve Springett, Creator/maintainer of CycloneDX among others',
    maintainer_email='steve.springett@owasp.org',
    url='https://github.com/CycloneDX/cyclonedx-python',
    license='Apache-2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7'
    ]
)