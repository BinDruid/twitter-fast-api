
FROM python:3.11-slim-bullseye
LABEL maintainer="bindruid"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./analytics/requirements.txt /code/
RUN pip install -r /code/requirements.txt

WORKDIR /code/
EXPOSE 50051
ENTRYPOINT ["python", "main.py"]

