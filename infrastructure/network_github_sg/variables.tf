variable "app_sg_group_name" {
  type    = string
  default = "github runner sg"
}

variable "app_ingress_from_port" {
  type    = list(number)
  default = [22]
}

variable "app_cidr_block" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

variable "app_protocol" {
  type    = string
  default = "tcp"
}

variable "app_ingress_to_port" {
  type    = list(number)
  default = [22]
}

variable "app_egress_from_port" {
  type    = number
  default = 0
}

variable "app_egress_to_port" {
  type    = number
  default = 65535
}