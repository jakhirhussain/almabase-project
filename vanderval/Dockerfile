# Use an official Python runtime as the base image
FROM python:3.5-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install PostgreSQL development libraries (required for psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends  build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . /app/

# Expose the port that Django will run on
EXPOSE 8000


# Run Django's migration and start the server when the container runs
CMD ["gunicorn", "vanderval.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
