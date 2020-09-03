FROM python:3.8-slim-buster
RUN pip install cyclonedx-bom
ENTRYPOINT ["cyclonedx-py"]
