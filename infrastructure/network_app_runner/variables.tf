variable "app_runner_service_name" {
  default = "bentoml_apprunner_service"
  type    = string
}

variable "app_runner_service_port" {
  default = 3000
  type    = number
}

variable "app_runner_service_image_url" {
  default = "566373416292.dkr.ecr.us-east-1.amazonaws.com/network_model:latest"
  type    = string
}

variable "app_runner_service_image_repository_type" {
  default = "ECR"
  type    = string
}

variable "app_runner_service_auto_deployments_enabled" {
  default = true
  type    = bool
}

variable "app_runner_service_cpu" {
  default = 1024
  type    = number
}

variable "app_runner_service_memory" {
  default = 2048
  type    = number
}

variable "app_runner_service_iam_service_role" {
  default = "AppRunnerECRAccessRole"
  type    = string
}

variable "app_runner_service_sleep_time" {
  default = "10s"
  type    = string
}