# =============================================================================
# Outputs for Production Environment
# =============================================================================

# VPC Outputs
output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "vpc_cidr" {
  description = "The CIDR block of the VPC"
  value       = module.vpc.vpc_cidr_block
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

# EC2 Outputs
output "web_server_id" {
  description = "The ID of the web server EC2 instance"
  value       = module.web_server.instance_id
}

output "web_server_public_ip" {
  description = "The public IP of the web server"
  value       = module.web_server.public_ip
}

output "web_server_private_ip" {
  description = "The private IP of the web server"
  value       = module.web_server.private_ip
}

# Connection Info
output "ssh_command" {
  description = "SSH command to connect to the web server"
  value       = "ssh -i <your-key.pem> ec2-user@${module.web_server.public_ip}"
}
