import argparse
import requirements
from cyclonedx import BomGenerator

parser = argparse.ArgumentParser(description='Add some integers.')

parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='interger list')
parser.add_argument('--sum', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

# args = parser.parse_args()
# print(args.sum(args.integers))


def main():
    with open('requirements.txt', 'r') as fd:
        print("Generating CycloneDX BOM")
        component_elements = []
        for req in requirements.parse(fd):
            if len(req.specs[0]) >= 2:
                name = req.name
                version = req.specs[0][1]
                if req.specs[0][0] != "==":
                    print("WARNING: " + name + " is not pinned to a specific version. Using: " + version)
                response = BomGenerator.get_package_info(name, version)
                if response:
                    json = response.json()
                    info = json["info"]
                    author = info["author"]
                    description = info["summary"]
                    license = info["license"]  # TODO: Attempt to perform SPDX license ID resolution
                    purl = BomGenerator.generate_purl(name, version)
                    component = BomGenerator.build_component_element(author, name, version, description, license, purl, "false")
                    component_elements.append(component)
                else:
                    # nothing to parse, simply add the name, version, and purl to bom
                    purl = BomGenerator.generate_purl(name, version)
                    component = BomGenerator.build_component_element("", name, version, "", "", purl, "false")
                    component_elements.append(component)

        BomGenerator.build_bom(component_elements)

main()