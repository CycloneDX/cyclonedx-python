#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os.path
from setuptools import setup, find_packages

script_path = os.path.dirname(__file__)

setup(
    name='cyclonedx-bom',
    version=open(os.path.join(script_path, 'VERSION')).read(),
    description='CycloneDX software bill-of-material (SBOM) generation utility',
    long_description=open(os.path.join(script_path, 'README.rst')).read(),
    packages=find_packages(),
    package_data={'cyclonedx.schema': ['bom-1.0.xsd', 'spdx.xsd']},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requirements_parser==0.2.0',
        'packageurl_python==0.8.7',
        'xmlschema==1.0.16',
        'requests==2.22.0',
        'packaging==19.2',
        'jsonschema==3.2.0',
    ],
    entry_points={
        'console_scripts': [
            'cyclonedx-py = cyclonedx.client:main'
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
        'Topic :: Security',
        'Topic :: Software Development',
        'Topic :: System :: Software Distribution',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ]
)
