#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='cyclonedx-bom',
    version='0.2.0',
    description='CycloneDX bill-of-material (BOM) generation utility',
    long_description=open("README.rst").read(),
    packages=find_packages(),
    package_data={'cyclonedx.schema': ['bom-1.0.xsd', 'spdx.xsd']},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requirements_parser==0.1.0',
        'packageurl_python==0.8.1',
        'xmlschema==1.0.7',
    ],
    entry_points={
        'console_scripts': [
            'cyclonedx-py = cyclonedx.cli.generateBom:main'
        ]
    },
    author='Steve Springett',
    author_email='steve.springett@owasp.org',
    maintainer='Steve Springett',
    maintainer_email='steve.springett@owasp.org',
    url='https://github.com/CycloneDX/cyclonedx-python',
    keywords=["BOM", "SBOM", "SCA"],
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
