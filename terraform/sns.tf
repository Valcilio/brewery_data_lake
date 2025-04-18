resource "aws_sns_topic" "brewery_etl_topic" {
  name = "brewery_etl_topic"
}

resource "aws_sns_topic_subscription" "user_updates_sqs_target" {
  topic_arn = aws_sns_topic.brewery_etl_topic.arn
  protocol  = "email"
  endpoint  = var.email
}