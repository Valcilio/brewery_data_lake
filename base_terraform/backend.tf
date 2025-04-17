terraform {
  backend "s3" {
    bucket = "ondad-terraform-state"
    key    = "ondad/brewery_data_lake"
    region = "us-east-1"
  }
}