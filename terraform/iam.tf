data "aws_iam_policy_document" "ondad_timeseries_etl_lambda_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "ondad_timeseries_etl_lambda_role_policy" {
  statement {
    sid       = "AllowS3OndadDashes"
    effect    = "Allow"
    actions   = ["s3:List*", "s3:DeleteObject", "s3:PutObject"]
    resources = ["arn:aws:s3:::ondad-dashboards-bucket", "arn:aws:s3:::ondad-dashboards-bucket/*", "arn:aws:s3:::ondad-raw-data-temp", "arn:aws:s3:::ondad-raw-data-temp/*"]
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
    resources = ["arn:aws:logs:us-east-1:311141538723:log-group:/aws/lambda/ondad_timeseries_etl_lambda*"]
  }
  statement {
    sid       = "AllowSecretsManager"
    effect    = "Allow"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = ["arn:aws:secretsmanager:us-east-1:311141538723:secret:API_KEYS*"]
  }
}

resource "aws_iam_policy" "ondad_timeseries_etl_lambda_policy" {
  name        = "ondad_timeseries_etl_lambda_policy"
  description = "Policy for Ondad Forecast Model Lambda Function"
  policy      = data.aws_iam_policy_document.ondad_timeseries_etl_lambda_role_policy.json
}

resource "aws_iam_role" "ondad_timeseries_etl_lambda_role" {
  name               = "ondad_timeseries_etl_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.ondad_timeseries_etl_lambda_assume_role_policy.json
}

resource "aws_iam_policy_attachment" "attach_to_ondad_timeseries_etl_role" {
  name       = "attach_to_ondad_timeseries_etl_role"
  roles      = [aws_iam_role.ondad_timeseries_etl_lambda_role.name]
  policy_arn = aws_iam_policy.ondad_timeseries_etl_lambda_policy.arn
}