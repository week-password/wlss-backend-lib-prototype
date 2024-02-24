FROM python:3.11-slim

WORKDIR /wlss-backend-lib

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install poetry==1.4.2

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

# needed to install our 'wlss' package (see "include = " in pyproject.toml)
COPY wlss ./wlss

# we also need to install 'test' dependencies here, because linters check tests code as well
# otherwise linters will report 'module not found' errors for tests code
RUN poetry install --with=lint,test

COPY . ./
