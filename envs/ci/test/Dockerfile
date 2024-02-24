FROM python:3.11-slim

WORKDIR /wlss-backend-lib

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install poetry==1.4.2

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

# needed to install our 'wlss' package (see "include = " in pyproject.toml)
COPY wlss ./wlss

RUN poetry install --with=test

COPY . ./
