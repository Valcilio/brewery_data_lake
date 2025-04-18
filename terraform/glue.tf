resource "aws_glue_catalog_database" "brewery_database" {
  name = "brewery_database"
}

resource "aws_iam_service_linked_role" "glue_service_role" {
  aws_service_name = "glue.amazonaws.com"
  custom_suffix    = "glue_service_role"
}

resource "aws_iam_role_policy" "brewery_etl_ec2_role_policy" {
  name   = "brewery_crawler_role_policy"
  role   = aws_iam_service_linked_role.glue_service_role.id
  policy = data.aws_iam_policy_document.brewery_ec2_role_policy.json
}

resource "aws_glue_crawler" "brewery_crawler" {
  database_name = aws_glue_catalog_database.brewery_database.name
  name          = "brewery_crawler"
  role          = aws_iam_service_linked_role.glue_service_role.arn

  s3_target {
    path = "s3://${aws_s3_bucket.brewery-gold-layer.bucket}"
  }
}