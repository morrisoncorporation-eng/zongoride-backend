# Use an official Python runtime as a parent image
FROM osgeo/gdal:python3.11-ubuntu-full-latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y python3-psycopg2

# Copy the requirements file and install dependencies
COPY mysite/requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /code/
