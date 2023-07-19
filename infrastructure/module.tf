terraform {
  backend "s3" {
    bucket = "network-ineuron-tf-state"
    key    = "tf_state"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

module "network_github_sg" {
  source = "./network_github_sg" 
}

# module "network_feature_store" {
#   source = "./network_feature_store"
# }

# module "network_app_artifacts" {
#   source = "./network_artifacts"
# }

# module "network_model_ecr" {
#   source = "./network_model_ecr"
# }

# module "network_app_runner" {
#   source = "./network_app_runner"
# }

# module "network_mlflow_instance" {
#   source = "./network_mlflow_instance"
# }