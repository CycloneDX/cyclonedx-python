# use pyproject from pep621
# use pyproject from poetry implementation


from typing import TYPE_CHECKING, Any, Dict, Iterator

from .pep621 import project2component, project2dependencies
from .poetry import poetry2component, poetry2dependencies
from .toml import toml_loads

if TYPE_CHECKING:  # pragma: no cover
    from cyclonedx.model.component import Component, ComponentType
    from packaging.requirements import Requirement


def pyproject2component(data: Dict[str, Any], *,
                        type: 'ComponentType') -> 'Component':
    tool = data.get('tool', {})
    if 'poetry' in tool:
        return poetry2component(tool['poetry'], type=type)
    if 'project' in data:
        return project2component(data['project'], type=type)
    raise ValueError('Unable to build component from pyproject')


def pyproject_load(pyproject_file: str) -> Dict[str, Any]:
    try:
        pyproject_fh = open(pyproject_file, 'rt', encoding='utf8', errors='replace')
    except OSError as err:
        raise ValueError(f'Could not open pyproject file: {pyproject_file}') from err
    with pyproject_fh:
        return toml_loads(pyproject_fh.read())


def pyproject_file2component(pyproject_file: str, *,
                             type: 'ComponentType') -> 'Component':
    return pyproject2component(
        pyproject_load(pyproject_file),
        type=type
    )


def pyproject2dependencies(data: Dict[str, Any]) -> Iterator['Requirement']:
    tool = data.get('tool', {})
    if 'poetry' in tool:
        return poetry2dependencies(tool['poetry'])
    if 'project' in data:
        return project2dependencies(data['project'])
    return iter(())
