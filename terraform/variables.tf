variable "aws_account_id" {
  description = "The ID of the AWS account."
  type        = string
}

variable "aws_region" {
  description = "The region of the AWS account."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "The name of the project."
  type        = string
  default     = "brewery_etl"
}

variable "email" {
  description = "The email address for SNS notifications."
  type        = string
}

variable "image_tag" {
  description = "The tag for the Docker image."
  type        = string
}