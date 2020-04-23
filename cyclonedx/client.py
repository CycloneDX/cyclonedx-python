#!/usr/bin/env python
# encoding: utf-8

# This file is part of CycloneDX Python module.
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
# Copyright (c) Steve Springett. All Rights Reserved.

import argparse
import sys

import chardet

from cyclonedx.bom import reader, generator, validator


def build_parser():
    parser = argparse.ArgumentParser(description='CycloneDX BOM Generator')
    parser.add_argument('-i', action="store", dest="input_file", default="requirements.txt")
    parser.add_argument('-o', action="store", dest="output_file", default="bom.xml")
    parser.add_argument(
        '--package-info-url',
        action="store",
        dest="package_info_url",
        default=reader.DEFAULT_PACKAGE_INFO_URL
    )
    return parser


def print_arguments(args):
    print("Input file: " + args.input_file)
    print("Output BOM: " + args.output_file)
    print("Package info url: " + args.package_info_url)


def generate_bom(args):
    if args.input_file == '-':
        bom_xml = reader.read_bom(sys.stdin, args.package_info_url)
    else:
        rawdata = open(args.input_file, 'rb').read()
        result = chardet.detect(rawdata)
        with open(args.input_file, 'r', encoding=result['encoding']) as fd:
            bom_xml = reader.read_bom(fd, args.package_info_url)
    return bom_xml


def write_bom(args, bom_xml):
    with open(args.output_file, "w", encoding="utf-8") as file:
        file.write(bom_xml)


def validate_bom(args):
    print("Validating BOM")
    if validator.is_valid(args.output_file):
        print("Complete")
    else:
        print("The generated BOM is not valid")


def main():
    parser = build_parser()
    args = parser.parse_args()
    print_arguments(args)

    bom_xml = generate_bom(args)
    write_bom(args, bom_xml)
    validate_bom(args)


if __name__ == "__main__":
    main()
