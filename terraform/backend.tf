terraform {
  backend "s3" {
    bucket = "ondad-terraform-state"
    key    = "ondad/brewery_data_lake_definitive"
    region = "us-east-1"
  }
}