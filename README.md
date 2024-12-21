# 📁 FileVault: Modern Full-Stack File Management Platform

A production-grade file management system built with modern technologies:
- **Backend**: Django 5.0 REST API
- **Frontend**: React TypeScript with TailwindCSS
- **Infrastructure**: AWS (S3, RDS, ECR) managed with Terraform
- **DevOps**: Docker containerization & GitHub Actions CI/CD
- **Security**: AWS IAM, secure file handling, input validation

[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/Terraform-AWS-purple.svg)](https://www.terraform.io/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-black.svg)](https://github.com/features/actions)

## 🚀 Features

- Secure file upload and storage in AWS S3
- Content management with AWS RDS MySQL
- Real-time file search and filtering
- Containerized development and deployment
- Automated CI/CD pipeline with GitHub Actions
- Infrastructure as Code with Terraform

## 🏗️ Architecture Overview

 see [Architecture Documentation](./docs/architecture.md).

## 🛠️ Tech Stack

### Backend
- Django 5.0 with Django REST Framework
- AWS SDK for Python (Boto3)
- MySQL on AWS RDS

### Frontend
- React with TypeScript
- TailwindCSS for styling
- Jest for testing

### Infrastructure
- Docker and Docker Compose
- AWS (S3, RDS, ECR)
- Terraform for IaC
- GitHub Actions for CI/CD

## 📚 Documentation

Detailed documentation can be found in the `/docs` directory:

- **[Project Architecture](./docs/architecture.md)**
  - System Overview
  - Component Interaction
  - Data Flow
  - Technology Stack Details

- **[AWS Infrastructure](./docs/aws-infrastructure.md)**
  - Infrastructure Overview
  - Resource Organization
  - Security Configuration
  - Terraform Setup and Deployment

- **[Backend Features](./docs/backend-features.md)**
  - API Endpoints
  - File Processing Service
  - AWS Integration
  - Atomic Transactions
  - Security Protection against SQL Injection
  - Error Handling
  - Testing Strategy

- **[Frontend Features](./docs/frontend-features.md)**
  - Component Structure
  - State Management
  - File Upload Flow
  - Search and Filter Functionality
  - Testing Implementation

- **[Infrastructure as Code (Terraform)](./docs/terraform.md)**
  - Resource Definitions
  - Variable Configuration
  - State Management
  - Module Organization
  - Deployment Instructions

- **[CI/CD Pipeline](./docs/ci-cd-pipeline.md)**
  - Pipeline Overview
  - GitHub Actions Configuration
  - ECR Integration
  - Deployment Strategy

- **[Setup Guide](./docs/setup-guide.md)**
  - Local Development Setup
  - Docker Configuration
  - Environment Variables
  - Database Setup
  - AWS Configuration

## 🚦 Getting Started

### Prerequisites
- Docker and Docker Compose
- AWS Account and CLI configured
- Terraform >= 1.0
- Node.js >= 18
- Python >= 3.11

### Quick Start
1. Clone the repository
```bash
git clone https://github.com/yourusername/file-loader.git
cd file-loader
```

2. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configurations
```

3. Start the application
```bash
docker-compose up -d
```

4. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- API Documentation: http://localhost:8000/api/docs

## 🧪 Testing Strategy

### Backend Testing

#### Unit Tests
- **Models & Serializers**
  ```bash
  docker-compose exec backend python manage.py test api.tests.test_models api.tests.test_serializers
  ```
  - File upload model validation
  - Serializer data transformation
  - Input validation & error handling

#### Integration Tests
- **API Endpoints**
  ```bash
  docker-compose exec backend python manage.py test api.tests.test_integration
  ```
  - Complete file upload flow
  - File listing and deletion
  - Error handling scenarios
  - S3 integration with mocked responses

#### Key Test Cases
```python
# File Upload Flow
test_file_upload()          # Tests successful file upload
test_file_upload_no_file()  # Tests error handling
test_invalid_file_type()    # Tests file validation
test_large_file_handling()  # Tests size restrictions

# Database & S3 Integration
test_upload_list_delete_flow()  # Tests complete lifecycle
test_s3_integration()          # Tests AWS integration
```

### Frontend Testing

#### Component Tests
- **React Testing Library**
  ```bash
  docker-compose exec frontend npm test
  ```
  - Component rendering
  - User interactions
  - State management
  - Error handling

#### Key Test Suites
```typescript
// App Component Tests
'renders without crashing'
'displays files when loaded'
'handles file upload'
'shows error messages'

```

### Running All Tests
```bash
# Backend tests
docker-compose exec backend python manage.py test

# Frontend tests
docker-compose exec frontend npm test
```

## 🌐 Deployment

The application can be deployed using:
1. Manual deployment using Docker Compose
2. Automated deployment via GitHub Actions
3. Infrastructure provisioning with Terraform

See the [deployment documentation](./docs/ci-cd-pipeline.md) for detailed instructions.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- AWS Documentation
- Django Documentation
- React Documentation
- Docker Documentation
- Terraform Documentation
