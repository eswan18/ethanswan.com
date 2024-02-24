# Testing

This folder contains a Python package for running tests against my site.


## Setting up

This is managed with [UV](https://github.com/astral-sh/uv).

The first time you use it, you'll need to set up a virtual environment:

```bash
uv venv
```

Then (every time) you'll activate it:

```
. .venv/bin/activate
```

Install this package with:

```bash
uv pip install -e ".[dev]"
```

## Running the suite.

```bash
pytest
```

By default, the suite runs against `https://ethanswan.com`.
However, it can be useful to run it against a different URL (probably a locally-running server).
Do that by setting the `ES_SITE_URL` environment variable:

```bash
ES_SITE_URL=http://localhost:1313 pytest
```
