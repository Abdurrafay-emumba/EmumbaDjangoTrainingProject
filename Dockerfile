# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copying the requirements.txt file
COPY requirements.txt .
# The psycopg==3.2.7 in our requirements file needs this libpq-dev to run. libpq-dev was not in the requirements.tx because it is a system binary and was not installed manually.
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean
# Installing the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project files
COPY . .

# Expose port (must match the one used in docker-compose)
EXPOSE 8000

# Default command — can be overridden in docker-compose
# You need the "0.0.0.0:8000", because the 8000 port that is being mapped is the one on 0.0.0.0
# By default, python manage.py runserver listens on 127.0.0.1 inside the container, which means the container itself accepts connections only from localhost inside the container — not from outside.
# You need to make Django listen on 0.0.0.0 so it accepts connections from anywhere inside the container network (which includes your host via port mapping).
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

