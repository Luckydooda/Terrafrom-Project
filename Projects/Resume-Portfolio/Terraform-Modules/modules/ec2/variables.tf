variable "ami_id" {
    type = string
    description = "The ID of the AMI to use for the EC2 instance"
}

variable "instance_type" {
    type = string
    description = "The type of the EC2 instance"
    default = "t2.micro"
}

variable "subnet_id" {
    type = string
    description = "The ID of the subnet to use for the EC2 instance"
}

variable "project_name" {
    type = string
    description = "The name of the project"
}

variable "environment" {
    type = string
    description = "The environment of the project"
}

variable "key_name" {
    type        = string
    description = "The name of the SSH key pair"
}

variable "vpc_id" {
    type        = string
    description = "The ID of the VPC"
}


