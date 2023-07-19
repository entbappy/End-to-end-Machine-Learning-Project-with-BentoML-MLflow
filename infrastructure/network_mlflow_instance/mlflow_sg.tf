resource "aws_security_group" "security_group" {
  name = var.mlflow_sg_group_name

  ingress {
    from_port   = var.mlflow_ingress_from_port[0]
    to_port     = var.mlflow_ingress_to_port[0]
    protocol    = var.mlflow_protocol
    cidr_blocks = var.mlflow_cidr_block
  }

  ingress {
    from_port   = var.mlflow_ingress_from_port[1]
    to_port     = var.mlflow_ingress_to_port[1]
    protocol    = var.mlflow_protocol
    cidr_blocks = var.mlflow_cidr_block
  }

  ingress {
    from_port   = var.mlflow_ingress_from_port[2]
    to_port     = var.mlflow_ingress_to_port[2]
    protocol    = var.mlflow_protocol
    cidr_blocks = var.mlflow_cidr_block
  }

  egress {
    from_port   = var.mlflow_egress_from_port
    to_port     = var.mlflow_egress_to_port
    protocol    = var.mlflow_protocol
    cidr_blocks = var.mlflow_cidr_block
  }

  tags = {
    Name = var.mlflow_sg_group_name
  }
}