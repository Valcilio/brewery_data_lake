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

resource "aws_iam_role" "brewery_etl_lambda_role" {
  name               = "brewery_etl_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


data "archive_file" "lambda_handler" {
    type = "zip"
    source_file = "lambda_handler.py"
    output_path = "lambda_handler.zip"
}

resource "aws_lambda_function" "brewery_etl_lambda" {
    function_name = "brewery_etl_lambda"
    filename = "lambda_handler.zip"
    source_code_hash = data.archive_file.lambda_handler.output_base64sha256
    runtime = "python3.10"
    handler = "lambda_handler.lambda_handler"
    role = aws_iam_role.brewery_etl_lambda_role.arn
}