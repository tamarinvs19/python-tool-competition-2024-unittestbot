# Python Tool Competition Implementation Using UnitTestBot

Uses the python-tool-competition-2024 to generate tests using the
UnitTestBot.

For more information see
<https://github.com/ThunderKey/python-tool-competition-2024/>.

## Requirements

* Python 3.11, implementation: CPython
* poetry
* OS: Linux
* Java 17, accessible in command line under name `java`
* glibc>=2.31

## Installation

* Install [poetry](https://python-poetry.org/)
* Run `poetry install`

## Development

The entry point called by `python-tool-competition-2024` is the `build_test`
method in `python_tool_competition_2024_unittestbot/generator.py`.

## Calculating Metrics

Run `poetry run python-tool-competition-2024 run unittestbot`.

With `poetry run python-tool-competition-2024 run -h` you can find out what
generators were detected.
