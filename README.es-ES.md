

# Twitter Minimal API

## Prerrequisitos

- `Python 3.11`
- `Postgresql 15`

## Desarrollo

### Ejemplo de `.env`

```shell
DEBUG=True
SECRET_KEY=super_secret_key
DB_URL=postgres://postgres:password@localhost/database_name
PAGINATION_PER_PAGE=20
JWT_SECRET=secret_key
JWT_ALG=HS256
JWT_EXP=86400
```

### Configuración de la base de datos

Ejecutar el servidor de base de datos

```shell
docker compose -f ./docker-compose-dev.yml up
```

Crear tu primera migración

```shell
alembic revision --autogenerate
```

Actualizar la base de datos cuando se creen nuevas migraciones

```shell
alembic upgrade head
```

### Ejecutar la aplicación FastAPI

```shell
make dev
```

Consulta la documentación de la API en `localhost:8000/docs` o `localhost:8000/redoc`

### Ejecutar migraciones de base de datos

```shell
make migrate
```

### Ejecutar pruebas

```shell
make test
```
