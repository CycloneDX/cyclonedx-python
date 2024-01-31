FROM python:3.12-slim

ARG VERSION

ARG CDX_PATH=/opt/cyclonedx-py
ARG CDX_VENV=${CDX_PATH}/venv

RUN mkdir -p "${CDX_PATH}"
RUN python -m venv --without-pip "${CDX_VENV}"
ENV VIRTUAL_ENV=${CDX_VENV}
ENV PATH=${VIRTUAL_ENV}/bin:${PATH}

COPY ./dist ${CDX_PATH}/dist
RUN pip --python "${CDX_VENV}" \
   install --no-cache-dir --no-input --progress-bar=off \
   --verbose --debug \
   --prefix "${CDX_VENV}" --require-virtualenv \
   --compile \
   "cyclonedx-bom==${VERSION}" --find-links "file://${CDX_PATH}/dist"
RUN rm -rf ${CDX_PATH}/dist

ENTRYPOINT ["cyclonedx-py"]
