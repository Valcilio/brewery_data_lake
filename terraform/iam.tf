data "aws_iam_policy_document" "assume_ec2_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "brewery_ec2_role_policy" {
  statement {
    sid     = "AllowS3BreweryBuckets"
    effect  = "Allow"
    actions = ["s3:GetObject", "s3:List*", "s3:DeleteObject", "s3:PutObject"]
    resources = [
      "arn:aws:s3:::brewery-bronze-layer*",
      "arn:aws:s3:::brewery-silver-layer*",
      "arn:aws:s3:::brewery-gold-layer*"
    ]
  }
  statement {
    sid       = "AllowECRGetImageAll"
    effect    = "Allow"
    actions   = ["ecr:GetAuthorizationToken", "ecr:BatchCheckLayerAvailability", "ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage"]
    resources = ["*"]
  }
  statement {
    sid       = "AllowCloudwatchLogs"
    effect    = "Allow"
    actions   = ["logs:*"]
    resources = ["arn:aws:logs:us-east-1:${var.aws_account_id}:log-group:/aws/ec2/brewery_etl_ec2*"]
  }
  statement {
    sid       = "AllowSnsPublish"
    effect    = "Allow"
    actions   = ["sns:Publish"]
    resources = ["arn:aws:sns:${var.aws_region}:${var.aws_account_id}:brewery_etl_topic*"]
  }
  statement {
    sid     = "AllowParameterStoreReadWrite"
    effect  = "Allow"
    actions = ["ssm:GetParameter", "ssm:PutParameter"]
    resources = [
      "arn:aws:ssm:${var.aws_region}:${var.aws_account_id}:parameter/brewery_start_page*"
    ]
  }
  statement {
    sid       = "AllowKMSDecrypt"
    effect    = "Allow"
    actions   = ["kms:*"]
    resources = ["arn:aws:kms:${var.aws_region}:${var.aws_account_id}:key/de3057e0-8fae-41a1-9432-563e2acb3c04*"]
  }
}

resource "aws_iam_role" "brewery_etl_ec2_role" {
  name               = "brewery_etl_ec2_role"
  assume_role_policy = data.aws_iam_policy_document.assume_ec2_role.json
}

resource "aws_iam_role_policy" "brewery_etl_ec2_role_policy" {
  name   = "brewery_etl_ec2_role_policy"
  role   = aws_iam_role.brewery_etl_ec2_role.id
  policy = data.aws_iam_policy_document.brewery_ec2_role_policy.json
}

resource "aws_iam_instance_profile" "brewery_etl_ec2_instance_profile" {
  name = aws_iam_role.brewery_etl_ec2_role.name
  role = aws_iam_role.brewery_etl_ec2_role.name
}
