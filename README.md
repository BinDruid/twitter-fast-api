# Twitter Minimal API




## Prerequisites

- `Python 3.11`
- `Postgresql 15`


## Development

### `.env` example

```shell
DEBUG=True
SECRET_KEY=super_secret_key
DB_URL=postgres://postgres:password@localhost/database_name
PAGINATION_PER_PAGE=20
JWT_SECRET=secret_key
JWT_ALG=HS256
JWT_EXP=86400
```

### Database setup

Run database server

```shell
docker compose -f ./docker-compose-dev.yml up
```

Create your first migration

```shell
alembic revision --autogenerate
```

Upgrading the database when new migrations are created

```shell
alembic upgrade head
```

### Run fastapi app

```shell
make dev
```

Check API documentation at `localhost:8000/docs` or `localhost:8000/redoc`

### Run database migrations

```shell
make migrate
```

### Run tests

```shell
make test
```
