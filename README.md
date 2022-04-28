# datasette-copy-to-memory

[![PyPI](https://img.shields.io/pypi/v/datasette-copy-to-memory.svg)](https://pypi.org/project/datasette-copy-to-memory/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-copy-to-memory?include_prereleases&label=changelog)](https://github.com/simonw/datasette-copy-to-memory/releases)
[![Tests](https://github.com/simonw/datasette-copy-to-memory/workflows/Test/badge.svg)](https://github.com/simonw/datasette-copy-to-memory/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-copy-to-memory/blob/main/LICENSE)

Copy database files into an in-memory database on startup

This plugin is **highly experimental**. It currently exists to support Datasette performance research, and is not designed for actual production usage.

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-copy-to-memory

## Usage

On startup, Datasette will create an in-memory named database for each attached database. This database will have the same name but with `_memory` at the end.

So running this:

    datasette fixtures.db

Will serve two databases: the original at `/fixtures` and the in-memory copy at `/fixtures_memory`.

## Configuration

By default every attached database file will be loaded into a `_memory` copy.

You can use plugin configuration to specify just a subset of the database. For example, to create `github_memory` but not `fixtures_memory` you would use the following `metadata.yml` file:

```yaml
plugins:
  datasette-copy-to-memory:
    databases:
    - github
```
Then start Datasette like this:

    datasette github.db fixtures.db -m metadata.yml

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-copy-to-memory
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
