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

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


data "archive_file" "lambda_test" {
    type = "zip"
    source_file = "lambda_test.py"
    output_path = "lambda_test.zip"
}

resource "aws_lambda_function" "brewery_test_lambda" {
    function_name = "brewery_test_lambda"
    filename = "lambda_test.zip"
    source_code_hash = data.archive_file.lambda_test.output_base64sha256
    runtime = "python3.10"
    handler = "lambda_test.lambda_handler"
    role = aws_iam_role.iam_for_lambda.arn
}