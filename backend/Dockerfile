# Use Python slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set build arguments
ARG DEBUG
ARG SECRET_KEY
ARG FRONTEND_URL
ARG AWS_REGION
ARG AWS_STORAGE_BUCKET_NAME
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG RDS_ENDPOINT
ARG DATABASE_NAME
ARG DATABASE_USER
ARG DATABASE_PASSWORD
ARG DATABASE_HOST
ARG DATABASE_PORT
ARG DJANGO_ENVIRONMENT

# Set environment variables
ENV DEBUG=$DEBUG \
    SECRET_KEY=$SECRET_KEY \
    FRONTEND_URL=$FRONTEND_URL \
    AWS_REGION=$AWS_REGION \
    AWS_STORAGE_BUCKET_NAME=$AWS_STORAGE_BUCKET_NAME \
    AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    RDS_ENDPOINT=$RDS_ENDPOINT \
    DATABASE_NAME=$DATABASE_NAME \
    DATABASE_USER=$DATABASE_USER \
    DATABASE_PASSWORD=$DATABASE_PASSWORD \
    DATABASE_HOST=$DATABASE_HOST \
    DATABASE_PORT=$DATABASE_PORT \
    DJANGO_ENVIRONMENT=$DJANGO_ENVIRONMENT

# Copy requirements file
COPY requirements.txt /app/

# install needed system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    python3-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]