# Use an official Python runtime as a base image
FROM python:3.12.0-alpine3.17

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore

RUN addgroup -S appgroup && adduser -S appuser -G appgroup -u 80

RUN \
  apk add \
  --no-cache \
  --no-progress \
  --update \
  build-base

COPY . /app
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Install deps and run build
RUN pip3 install --no-cache-dir pipenv \
  && pipenv install --system --deploy --ignore-pipfile

USER 80
EXPOSE 5000
CMD ["pipenv", "run", "flask", "run", "--host", "0.0.0.0"]
