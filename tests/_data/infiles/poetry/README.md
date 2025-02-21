poetry lock file version -- preferred poetry versions:
- `1.0` -> poetry==1.0.10
- `1.1` -> poetry==1.1.15
- `2.0` -> poetry==1.8.5
- `2.1` -> poetry==2.x

!! remove [poetry cache dir](https://python-poetry.org/docs/configuration/#cache-directory),
when switching versions:
- `rm -rf "$HOME/.cache/pypoetry" "$XDG_CACHE_HOME/pypoetry"`
- `poetry cache clear --all PyPI`
