# app-event-management

## Local development environment

We use [Poetry](https://python-poetry.org/) to manage dependencies.

```console
poetry install
```

Run development server:

```console
export SECRET_KEY="secret_key"
make dev
```

Run unit tests with:

```console
make test
```
