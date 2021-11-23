FROM python:3.10-slim-buster

ARG VERSION

RUN pip install cyclonedx-bom==${VERSION}
ENTRYPOINT ["cyclonedx-bom"]
