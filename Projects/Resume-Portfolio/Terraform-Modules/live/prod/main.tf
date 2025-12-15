# =============================================================================
# Production Environment - Root Module
# =============================================================================
# This file combines VPC and EC2 modules to create a complete infrastructure

terraform {
  required_version = ">= 1.0.0"

  # Remote State Configuration
  backend "s3" {
    bucket         = "laxmi-terraform-state-2024"
    key            = "prod/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock-table"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Provider Configuration
provider "aws" {
  region = var.aws_region
}

# =============================================================================
# VPC Module
# =============================================================================
module "vpc" {
  source = "../../modules/vpc"

  vpc_cidr           = var.vpc_cidr
  project_name       = var.project_name
  environment        = var.environment
  public_subnets     = var.public_subnets
  private_subnets    = var.private_subnets
  availability_zones = var.availability_zones
}

# =============================================================================
# EC2 Module - Web Server
# =============================================================================
module "web_server" {
  source = "../../modules/ec2"

  ami_id        = var.ami_id
  instance_type = var.instance_type
  subnet_id     = module.vpc.public_subnet_ids[0] # Launch in first public subnet
  vpc_id        = module.vpc.vpc_id
  key_name      = var.key_name
  project_name  = var.project_name
  environment   = var.environment
}
