# llm-templates-github

[![PyPI](https://img.shields.io/pypi/v/llm-templates-github.svg)](https://pypi.org/project/llm-templates-github/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-templates-github?include_prereleases&label=changelog)](https://github.com/simonw/llm-templates-github/releases)
[![Tests](https://github.com/simonw/llm-templates-github/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-templates-github/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-templates-github/blob/main/LICENSE)

Laod LLM templates from GitHub repositories

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-templates-github
```
## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-templates-github
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
