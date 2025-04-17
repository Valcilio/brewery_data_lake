resource "aws_cloudwatch_log_group" "ondad_timeseries_etl_lambda_log_group" {
  name              = "/aws/lambda/ondad_timeseries_etl_lambda"
  retention_in_days = 1
}