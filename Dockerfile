# Use an official Python runtime as a parent image
FROM ghcr.io/osgeo/gdal:ubuntu-full-3.11.4

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /code

# Install build dependencies for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev build-essential python3-pip python3-full && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file and install dependencies
COPY mysite/requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /code/

# Expose port for the web application
EXPOSE 8000
