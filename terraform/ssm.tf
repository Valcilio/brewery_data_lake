resource "aws_ssm_parameter" "brewery_start_page" {
  name      = "brewery_start_page"
  type      = "String"
  value     = "1"
}