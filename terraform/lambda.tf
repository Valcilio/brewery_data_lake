data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "brewery_lambda_role_policy" {
  statement {
    sid       = "AllowEC2FullAccess"
    effect    = "Allow"
    actions   = ["ec2:*"]
    resources = ["*"]
  }
  statement {
    sid       = "AllowCloudwatchLogs"
    effect    = "Allow"
    actions   = ["logs:*"]
    resources = ["arn:aws:logs:us-east-1:${var.aws_account_id}:log-group:/aws/lambda/brewery_etl_lambda*"]
  }
  statement {
    sid       = "AllowSnsPublish"
    effect    = "Allow"
    actions   = ["sns:Publish"]
    resources = ["arn:aws:sns:${var.aws_region}:${var.aws_account_id}:brewery_etl_topic*"]
  }
  statement {
    sid       = "AllowPassRoleToEC2"
    effect    = "Allow"
    actions   = ["iam:PassRole"]
    resources = [aws_iam_role.brewery_etl_ec2_role.arn]
  }
}

resource "aws_iam_role" "brewery_etl_lambda_role" {
  name               = "brewery_etl_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy" "brewery_etl_lambda_role_policy" {
  name   = "brewery_etl_lambda_role_policy"
  role   = aws_iam_role.brewery_etl_lambda_role.id
  policy = data.aws_iam_policy_document.brewery_lambda_role_policy.json
}

data "archive_file" "lambda_handler" {
  type        = "zip"
  source_file = "lambda_handler.py"
  output_path = "lambda_handler.zip"
}

resource "aws_lambda_function" "brewery_etl_lambda" {
  function_name    = "brewery_etl_lambda"
  filename         = "lambda_handler.zip"
  source_code_hash = data.archive_file.lambda_handler.output_base64sha256
  runtime          = "python3.10"
  handler          = "lambda_handler.lambda_handler"
  role             = aws_iam_role.brewery_etl_lambda_role.arn
  environment {
    variables = {
      "ECR_IMAGE_NAME"       = "brewery_etl_ecr_repo"
      "ECR_IMAGE_TAG"        = "${var.image_tag}"
      "EC2_INSTANCE_PROFILE" = "${aws_iam_instance_profile.brewery_etl_ec2_instance_profile.name}"
    }
  }
}