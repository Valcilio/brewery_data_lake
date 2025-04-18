data "aws_kms_key" "get_brewery_kms_key" {
  key_id = "alias/brewery_etl_key"
}