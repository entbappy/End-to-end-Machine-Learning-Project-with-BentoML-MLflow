variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "artifacts_bucket_name" {
  type    = string
  default = "network-artifacts"
}

variable "aws_account_id" {
  type    = string
  default = "566373416292"
}

variable "force_destroy_bucket" {
  type    = bool
  default = true
}
