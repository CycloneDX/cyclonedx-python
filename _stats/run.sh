#!/usr/bin/env bash
set -xue

TFORMAT='%C ; %c ; %E ; %e ; %F ; %M ; %P ; %R ; %R ; %S ; %U ; %w ; %x'
SFILE='_stats/requirements.csv'


for i in tests/_data/infiles/environment/*
do
  if [[ ! "$i" =~ "broken" ]]
  then
    /bin/time -f "$TFORMAT" -a -o "$SFILE" \
    cyclonedx-py environment -o /dev/null --pyproject "$i"/pyproject.toml "$i"/.venv
  fi
done

for i in tests/_data/infiles/pipenv/*
do
  /bin/time -f "$TFORMAT" -a -o "$SFILE" \
  cyclonedx-py pipenv -o /dev/null --pyproject "$i"/pyproject.toml "$i"
done

for i in tests/_data/infiles/poetry/*/lock*
do
  /bin/time -f "$TFORMAT" -a -o "$SFILE" \
  cyclonedx-py poetry -o /dev/null "$i"
done

for i in tests/_data/infiles/requirements/*.txt
do
  /bin/time -f "$TFORMAT" -a -o "$SFILE" \
  cyclonedx-py requirements --pyproject tests/_data/infiles/requirements/pyproject.toml \
    -o /dev/null "$i"
done
