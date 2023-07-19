resource "random_integer" "random" {
  min = 1
  max = 50000
}

resource "aws_s3_bucket" "feature_store_bucket" {
  bucket        = "${random_integer.random.id}${var.feature_store_bucket_name}"
  force_destroy = var.force_destroy_bucket
}