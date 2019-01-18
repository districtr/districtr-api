# Districtr API

[![Build Status](https://dev.azure.com/gerrymandr/districtr/_apis/build/status/mggg.districtr-api?branchName=master)](https://dev.azure.com/gerrymandr/districtr/_build/latest?definitionId=2&branchName=master)

This repo holds the source code for the Districtr API. The API is written in Flask with a PostGIS database layer. We try to follow

## Development

### Installing and managing dependencies

We use [pipenv](https://pipenv.readthedocs.io/en/latest/) to install PyPI packages.

### Testing

We use the [pytest](https://docs.pytest.org/en/latest/) unit test framework. Our goal is to have comprehensive test coverage.

### Style

We use [flake8](http://flake8.pycqa.org/en/latest/) to enforce code style, but we set `max-line-length=88`.
We recommend the [black](https://black.readthedocs.io/en/stable/) source code formatter.
