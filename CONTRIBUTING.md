# Contributing

Feel free to open pull requests.

## Setup

This project uses [poetry]. Have it installed and setup first.

To install dev-dependencies and tools:

```shell
poetry install
```

## Code style

This project uses [PEP8] Style Guide for Python Code.  
Get it applied via:

```shell
poetry run autopep8 --in-place -r .
```

## Testing

```shell
poetry run tox
```

## Sign your commits

Please sign your commits,
to show that you agree to publish your changes under the current terms and licenses of the project.

```shell
git commit --signed-off ...
```

[poetry]: https://python-poetry.org