resource "aws_cloudwatch_log_group" "brewery_etl_lambda" {
  name              = "/aws/lambda/brewery_etl_lambda"
  retention_in_days = 3
}

resource "aws_cloudwatch_log_group" "brewery_etl_ec2" {
  name              = "/aws/ec2/brewery_etl_ec2"
  retention_in_days = 3
}