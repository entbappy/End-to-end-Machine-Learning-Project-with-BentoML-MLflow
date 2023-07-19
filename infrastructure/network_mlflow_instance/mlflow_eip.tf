resource "aws_eip" "elastic_ip" {
  vpc      = var.mlflow_eip_vpc
  instance = aws_instance.mlflow_instance.id
  tags = {
    Name = var.mlflow_eip_name
  }
}