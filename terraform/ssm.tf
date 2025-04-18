resource "aws_ssm_parameter" "foo" {
  name  = "brewery_start_page"
  type  = "String"
  value = "1"
}