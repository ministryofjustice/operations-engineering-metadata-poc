# Use an official Python runtime as a base image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN addgroup --gid 1017 --system appgroup \
  && adduser --system --uid 1017 --group appgroup

RUN apt update -y && apt dist-upgrade -y && apt install -y

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary packages and dependencies
RUN pip install --no-cache-dir -r requirements.txt

USER 1017
# Make port 5000 available to the world outside this container
EXPOSE 4567

# Run app.py when the container launches
CMD ["flask", "run"]

