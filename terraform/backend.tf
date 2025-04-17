terraform {
  backend "s3" {
    bucket = "ondad-terraform-state"
    key    = "ondad/timeseries_etl"
    region = "us-east-1"
  }
}