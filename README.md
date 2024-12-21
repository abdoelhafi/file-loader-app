
# FILE LOADER: Dockerized Django Web Application with AWS Integration

A web application that allows users to upload and manage text files, with content stored in AWS RDS and files in S3.

## Project Structure

project-root/
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── __init__.py
│   │   └── files/
│   │       ├── __init__.py
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── views.py
│   │       ├── urls.py
│   │       └── tests/
│   │           ├── __init__.py
│   │           ├── test_models.py
│   │           └── test_views.py
│   └── utils/
│       ├── __init__.py
│       ├── aws.py
│       └── validators.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── public/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── FileUpload.tsx
│   │   │   ├── FileList.tsx
│   │   │   └── SearchFiles.tsx
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   └── types.ts
│   │   └── styles/
│   │       └── globals.css
│   └── tests/
│       └── components/
│           └── FileUpload.test.tsx
├── docs/
│   ├── architecture.md
│   ├── aws-setup.md
│   ├── development.md
│   └── deployment.md
├── docker/
│   ├── nginx/
│   │   └── nginx.conf
│   └── mysql/
│       └── init.sql
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml

## Tech Stack

- Backend: Django 5.0
- Frontend: Next.js
- Database: AWS RDS (MySQL)
- Storage: AWS S3
- Containerization: Docker
- CI/CD: GitHub Actions

## Prerequisites

- Docker and Docker Compose
- AWS Account
- Python 3.11+
- Node.js 18+

## Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Copy the example environment file:
```bash
cp .env.example .env
```

3. Start the development environment:
```bash
docker-compose up -d
```

4. Access the application:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000

## Testing

```bash
# Run backend tests
docker-compose exec backend python manage.py test

# Run frontend tests
docker-compose exec frontend npm test
```

## Documentation

Detailed documentation for setup, deployment, and development can be found in the `docs/` directory.

## License

MIT