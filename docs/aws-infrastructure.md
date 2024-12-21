# AWS Infrastructure Architecture

## Table of Contents
- [Overview](#overview)
- [Network Architecture](#network-architecture)
- [Storage Services](#storage-services)
- [Database Configuration](#database-configuration)
- [Security Implementation](#security-implementation)
- [Infrastructure Management](#infrastructure-management)

## Overview

The infrastructure is deployed on AWS using Infrastructure as Code (Terraform) with a focus on security, scalability, and high availability. The architecture follows AWS best practices for a production environment.

## Network Architecture

### VPC Configuration
- **CIDR Block**: 10.0.0.0/16
- **DNS Support**: Enabled
- **DNS Hostnames**: Enabled

### Subnet Layout
```
├── Private Subnets
│   ├── private-1 (10.0.1.0/24) - AZ: us-east-1a
│   └── private-2 (10.0.2.0/24) - AZ: us-east-1b
└── Public Subnets
    ├── public-1 (10.0.10.0/24) - AZ: us-east-1a
    └── public-2 (10.0.11.0/24) - AZ: us-east-1b
```

### Network Components
- **Internet Gateway**: Enables internet access for public subnets
- **NAT Gateway**: Provides internet access for private subnets
- **Route Tables**:
  - Public Route Table: Routes traffic through Internet Gateway
  - Private Route Table: Routes traffic through NAT Gateway

## Storage Services

### S3 Configuration
- **Bucket Naming**: `${project_name}-${environment}-storage`
- **Security Features**:
  - Server-side encryption (AES256)
  - Versioning enabled
  - Public access blocked
  - ACLs disabled
- **Access Control**:
  - Private bucket policy
  - Encrypted data at rest

## Database Configuration

### RDS Instance Specifications
- **Engine**: MySQL 8.0
- **Instance Class**: db.t3.micro
- **Storage**:
  - Type: GP2 (SSD)
  - Size: 20GB
  - Encryption: Enabled
- **High Availability**:
  - Multi-AZ: Configured for development (false)
  - Subnet Group: Spans multiple AZs

### Backup Configuration
- Retention Period: 7 days
- Backup Window: 03:00-04:00 UTC
- Maintenance Window: Monday 04:00-05:00 UTC

## Security Implementation

### Network Security
- **VPC Security Groups**:

    RDS Security Group: Allow ingres traffic to the database from local ip (will be replaced in prod by security group of the backend server)

### Access Control
1. **Database Access**:
   - Port: 3306 (MySQL)
   - Private subnet placement
   - Security group restrictions
   - Allowed IP restrictions

2. **S3 Access**:
   - Block all public access
   - Encryption in transit and at rest
   - IAM role-based access

## Infrastructure Management

### Environment Variables
```hcl
Required Variables:
- aws_region (default: us-east-1)
- environment (default: dev)
- project_name (default: file-manager)
- db_username (sensitive)
- db_password (sensitive)
- db_name (default: filemanager)
- allowed_ip
```