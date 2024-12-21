# Setup Guide

## Table of Contents
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Docker Configuration](#docker-configuration)
- [Running the Application](#running-the-application)
- [Development Workflow](#development-workflow)

## Prerequisites

- Docker and Docker Compose
- AWS Account with configured S3 and RDS (see Terraform part)
- Git

## Environment Setup

### 1. Backend Environment (.env)

Create `backend/.env`:
```env
# Django Settings
DEBUG=1
SECRET_KEY=your-secret-key
FRONTEND_URL=http://localhost:3000

# AWS Configuration
AWS_REGION=your-region
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Database Configuration
DATABASE_NAME=your-db-name
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=your-db-host
DATABASE_PORT=3306
```

### 2. Frontend Environment

Create `frontend/.env`:
```env
FRONTEND_URL=http://localhost:8000/api
```

## Docker Configuration

### Project Structure
```
.
├── terraform
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── Dockerfile
    ├── package.json
    └── .env
```

## Running the Application

1. **Build and Start Services**
```bash
# First time build
docker-compose up --build

# Subsequent runs
docker-compose up
```

2. **Verify Services**
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

3. **View Logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Development Workflow

### Running Migrations
```bash
docker-compose exec backend python manage.py migrate
```

### Creating Admin User
```bash
docker-compose exec backend python manage.py createsuperuser
```

### Running Tests

Backend:
```bash
docker-compose exec backend python manage.py test
```

Frontend:
```bash
docker-compose exec frontend npm test
```
