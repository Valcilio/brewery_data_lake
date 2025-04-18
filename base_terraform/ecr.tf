resource "aws_ecr_repository" "brewery_etl_ecr_repo" {
name                 = "brewery_etl_ecr_repo"
image_tag_mutability = "MUTABLE"
}