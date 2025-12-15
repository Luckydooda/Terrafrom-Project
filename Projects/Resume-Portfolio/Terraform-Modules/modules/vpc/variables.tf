variable "vpc_cidr" {
    description = "The CIDR Block for the VPC"
    type        = string                # STRING not list!
    default     = "10.0.0.0/16"         # No brackets!
}

variable "project_name" {
    description = "The name of the project"
    type = string
}

variable "environment" {
    description = "The environment name"
    type = string
}

variable "public_subnets" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnets" {
    description = "List of private subnet CIDR blocks"
    type        = list(string)
    default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}