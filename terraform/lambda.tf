resource "aws_lambda_function" "ondad_timeseries_etl_lambda" {
  function_name = "ondad_timeseries_etl_lambda"
  role          = aws_iam_role.ondad_timeseries_etl_lambda_role.arn
  image_uri     = "${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${var.project_name}@${data.aws_ecr_image.ondad_timeseries_etl_ecr_repo_image.id}"
  package_type  = "Image"
  timeout       = 900
  memory_size   = 3008

  ephemeral_storage {
    size = 3008
  }
}