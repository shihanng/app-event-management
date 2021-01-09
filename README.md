# app-event-management

## Local development environment

We use [Poetry](https://python-poetry.org/) to manage dependencies.

```console
poetry install
```

Run development server:

```console
export SECRET_KEY="secret_key"
export DEBUG=true
export EMAIL_CONFIG="smtp://username@gmail.com:PASSWORD@smtp.gmail.com:587"
export NOTIFY_TO="notifg@example.com"
make dev
```

`EMAIL_CONFIG` consists of username, password, host name, and port number of the SMTP server for sending notification email. We can omit both `EMAIL_CONFIG` and `NOTIFY_TO` in development. In this case, the app will log a warning instead of sending email.

REST endpoints documentation is available as Swagger API documentation. See: http://localhost:5000/swagger/ after launching the development server.

Run unit tests with:

```console
make test
```

## UI

UI is available in <https://github.com/shihanng/app-event-management-ui>.
