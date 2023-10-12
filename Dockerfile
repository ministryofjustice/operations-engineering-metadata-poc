# Use an official Python runtime as a base image
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore

RUN addgroup --gid 80 --system appgroup \
  && adduser --system --uid 80 --group appgroup

RUN apt-get update && \
        apt-get upgrade -y

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

USER 80
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]
