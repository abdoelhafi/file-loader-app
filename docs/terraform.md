# Infrastructure as Code (Terraform)

## Table of Contents
- [Prerequisites](#prerequisites)
- [Configuration Setup](#configuration-setup)
- [Resource Overview](#resource-overview)
- [Deployment Steps](#deployment-steps)
- [State Management](#state-management)

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.0
- Access to AWS Console for initial setup
- Your local IP address for RDS access

## Configuration Setup

### 1. Create terraform.tfvars

Create a `terraform.tfvars` file with your specific values:

```hcl
# terraform.tfvars
aws_region     = "us-east-1"
environment    = "dev"           # or "prod"
project_name   = "file-vault"
db_username    = "admin"         # Choose a secure username
db_password    = "your-secure-password"
db_name        = "filemanager"
allowed_ip     = "YOUR.IP.ADD.RESS/32"  # Your IP in CIDR format
```

### 2. Optional Variables

You can also modify these default values in variables.tf:
```hcl
aws_region   = "us-east-1"    # Default region
environment  = "dev"          # Environment name
project_name = "file-manager" # Project identifier
```

## Resource Overview

The infrastructure creates:

```plaintext
├── VPC (10.0.0.0/16)
├── Subnets
│   ├── Private Subnets (2)
│   └── Public Subnets (2)
├── Security
│   ├── Internet Gateway
│   ├── NAT Gateway
│   └── Route Tables
├── Database
│   └── RDS MySQL Instance
└── Storage
    └── S3 Bucket
```

## Deployment Steps

### 1. Initialize Terraform

```bash
# Initialize Terraform and download providers
terraform init
```

### 2. Validate Configuration

```bash
# Check for configuration errors
terraform validate

# Format configuration files
terraform fmt
```

### 3. Review Plan

```bash
# See planned changes
terraform plan
```

### 4. Apply Infrastructure

```bash
# Deploy infrastructure
terraform apply
```

### 5. Verify Deployment

Access the outputs:
```bash
terraform output

# Outputs will include:
# - s3_bucket_name
# - s3_bucket_arn
# - rds_endpoint
# - rds_port
# - db_name
```

### 6. Infrastructure Updates

To update infrastructure:
```bash
# Make changes to .tf files
terraform plan
terraform apply tfplan
```

## State Management

### Local State
The current configuration uses local state. For team environments, consider:

1. Remote State Setup:
```hcl
terraform {
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "file-vault/terraform.tfstate"
    region = "us-east-1"
  }
}
```

2. State Commands:
```bash
# View current state
terraform show

# List resources
terraform state list

# Remove resource from state
terraform state rm [resource]
```

## Clean Up

To destroy infrastructure:
```bash
# Review destruction plan
terraform plan -destroy

# Destroy resources
terraform destroy -auto-approve
```

⚠️ **Warning**: This will delete all resources including:
- All data in RDS
- All files in S3
- All network infrastructure

## Security Notes

1. **Sensitive Variables**:
   - Never commit `terraform.tfvars` to version control
   - Use AWS Secrets Manager for production credentials
   - Enable S3 versioning for state files if using remote state

2. **Network Security**:
   - RDS is in private subnets
   - S3 bucket has public access blocked
   - Security groups limit access appropriately