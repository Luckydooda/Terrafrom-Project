resource "aws_instance" "main" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  key_name               = var.key_name
  tags = {
    Name        = "${var.project_name}-${var.environment}-ec2"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Security Group
resource "aws_security_group" "ec2_sg" {
  name   = "${var.project_name}-${var.environment}-ec2-sg"
  vpc_id = var.vpc_id # We need VPC ID! Add to variables!

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # SSH from anywhere (dev only!)
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # Allow all outbound
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-ec2-sg"
  }
}
