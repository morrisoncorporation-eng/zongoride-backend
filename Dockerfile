# Use an official Python runtime as a parent image
FROM ghcr.io/osgeo/gdal:alpine-small-3.11.4

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install build dependencies for Python packages
RUN apk add --no-cache postgresql-dev build-base

# Copy the requirements file and install dependencies
COPY mysite/requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /code/
