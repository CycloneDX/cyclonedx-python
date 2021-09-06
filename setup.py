#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os.path

from setuptools import setup, find_packages

script_path = os.path.dirname(__file__)

setup(
    name='cyclonedx-bom',
    version=open(os.path.join(script_path, 'VERSION')).read(),
    url='https://github.com/CycloneDX/cyclonedx-python',
    author='Steve Springett',
    author_email='steve.springett@owasp.org',
    maintainer='Steve Springett',
    maintainer_email='steve.springett@owasp.org',
    description='CycloneDX Software Bill of Materials (SBOM) generation utility',
    long_description=open(os.path.join(script_path, 'README.rst')).read(),
    long_description_content_type="text/markdown",
    keywords=["BOM", "SBOM", "SCA", "OWASP"],
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: System Administrators',
        'Topic :: Security',
        'Topic :: Software Development',
        'Topic :: System :: Software Distribution',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    data_files=[('', ['README.rst', 'requirements.txt', 'requirements-test.txt', 'VERSION'])],
    install_requires=open(os.path.join(script_path, 'requirements.txt')).read(),
    entry_points={
        'console_scripts': [
            'cyclonedx-py=cyclonedx_py.client:main'
        ]
    },
    zip_safe=False
)
