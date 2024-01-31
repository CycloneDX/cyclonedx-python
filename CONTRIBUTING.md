# Contributing

Pull requests are welcome.
But please read the
[CycloneDX contributing guidelines](https://github.com/CycloneDX/.github/blob/master/CONTRIBUTING.md)
first.

## Setup

This project uses [poetry]. Have it installed and setup first.

To install dev-dependencies and tools:

```shell
poetry install
```

## Code style

This project uses [PEP8] Style Guide for Python Code.  
This project loves sorted imports.  
Get it all applied via:

```shell
poetry run isort .
poetry run autopep8 -ir cyclonedx_py/ tests/
```

This project prefers `f'strings'` over `'string'.format()`.  
This project prefers `'single quotes'` over `"double quotes"`.  
This project prefers `lower_snake_case` variable names.

## Documentation

This project uses [Sphinx] to generate documentation which is automatically published to [RTFD][link_rtfd].

Source for documentation is stored in the `docs` folder in [RST] format.

You can generate the documentation locally by running:

```shell
cd docs
pip install -r requirements.txt
make html
```

## Testing

```shell
poetry run tox run
```

## Sign off your commits

Please sign off your commits, to show that you agree to publish your changes under the current terms and licenses of the project
, and to indicate agreement with [Developer Certificate of Origin (DCO)](https://developercertificate.org/).

```shell
git commit --signoff ...
```

[poetry]: https://python-poetry.org
[PEP8]: https://www.python.org/dev/peps/pep-0008/
[Sphinx]: https://www.sphinx-doc.org/
[link_rtfd]: https://cyclonedx-bom-tool.readthedocs.io/
[RST]: https://en.wikipedia.org/wiki/ReStructuredText
