
FROM python:3.11-slim-bullseye
LABEL maintainer="bindruid"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./analytics/requirements.txt /code/
RUN pip install -r /code/requirements.txt

RUN apt-get update && apt-get install -y curl

WORKDIR /code/
EXPOSE 8030
HEALTHCHECK CMD curl --fail http://localhost:8030/docs || exit 1
CMD fastapi run ./api/main.py --reload --host 0.0.0.0 --port 8030

