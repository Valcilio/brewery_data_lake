data "aws_iam_policy_document" "assume_glue_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_glue_catalog_database" "brewery_database" {
  name = "brewery_database"
}

resource "aws_iam_role" "glue_crawler_role" {
  name               = "AWSGlueServiceRole-glue_crawler_role"
  assume_role_policy = data.aws_iam_policy_document.assume_glue_role.json
}

resource "aws_iam_role_policy" "brewery_crawler_role_role_policy" {
  name   = "brewery_crawler_role_policy"
  role   = aws_iam_role.glue_crawler_role.id
  policy = data.aws_iam_policy_document.brewery_ec2_role_policy.json
}

resource "aws_glue_crawler" "brewery_crawler" {
  database_name = aws_glue_catalog_database.brewery_database.name
  name          = "brewery_crawler"
  role          = aws_iam_role.glue_crawler_role.arn
  schedule      = "cron(0 12 * * ? *)"
  s3_target {
    path = "s3://${aws_s3_bucket.brewery-gold-layer.bucket}"
  }
}