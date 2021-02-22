FROM python:3.9.2-slim-buster

ARG VERSION

COPY ./dist /tmp/dist
RUN pip install cyclonedx-bom==${VERSION} --find-links file:///tmp/dist
ENTRYPOINT ["cyclonedx-py"]
