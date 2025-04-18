data "aws_caller_identity" "current" {}

resource "aws_kms_key" "brewery_kms_key" {
  description             = "KMS Key fro Brewery Project"
  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "key-default-1"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        },
        Action   = "kms:*"
        Resource = "*"
      }
    ]
  })
}

resource "aws_kms_alias" "brewery_kms_key_alias" {
  name          = "alias/brewery_etl_key"
  target_key_id = aws_kms_key.brewery_kms_key.key_id
}