resource "aws_apprunner_service" "test_app_apprunner_service" {
  service_name = var.app_runner_service_name
  source_configuration {
    image_repository {
      image_configuration {
        port = var.app_runner_service_port
      }
      image_identifier      = var.app_runner_service_image_url
      image_repository_type = var.app_runner_service_image_repository_type
    }
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner-service-role.arn
    }

    auto_deployments_enabled = var.app_runner_service_auto_deployments_enabled
  }
  instance_configuration {
    cpu    = var.app_runner_service_cpu
    memory = var.app_runner_service_memory
  }
  depends_on = [
    time_sleep.wait_for_n_seconds
  ]
}

resource "time_sleep" "wait_for_n_seconds" {
  depends_on = [
    aws_iam_role.apprunner-service-role, aws_iam_role_policy_attachment.apprunner-service-role-attachment
  ]
  create_duration = var.app_runner_service_sleep_time
}