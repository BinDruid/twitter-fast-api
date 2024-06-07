
FROM python:3.11-slim-bullseye
LABEL maintainer="bindruid"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /code/
COPY ./alembic.ini /code/
RUN apt-get update && apt-get install -y curl
RUN pip install -r /code/requirements.txt

WORKDIR /code/
EXPOSE 8000
HEALTHCHECK CMD curl --fail http://localhost:8000/api/v1/healthcheck/ || exit 1
ENTRYPOINT ["fastapi", "run", "./twitter_api/main.py", "--reload", "--host", "0.0.0.0", "--port", "8000"]
