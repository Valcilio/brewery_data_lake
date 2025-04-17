"""Test the BreweryWritter class."""
from domain.usecases.brewerywritter import BreweryWritter

# def test_write_df_to_s3_as_parquet_with_kms_key(
#         test_parquet_raw: str, test_s3_path: str, test_kms_key: str, partition_cols: list
# ):
#     """Test the write_df_to_s3_as_parquet_with_kms_key method of BreweryWritter.
    
#     Args:
#         test_parquet_raw (str): The raw Parquet data for testing.
#         test_s3_path (str): The S3 path for testing.
#         test_kms_key (str): The KMS key for testing.
#         partition_cols (list): The partition columns for testing.
#     """
#     response = BreweryWritter(test_kms_key).write_df_to_s3_as_parquet_with_kms_key(test_parquet_raw, test_s3_path, partition_cols)

#     assert response["StatusCode"] == 200

def test_write_df_to_s3_as_parquet_with_kms_key_must_fail(
        test_parquet_raw: str, test_kms_key: str, partition_cols: list
):
    """Test if the write_df_to_s3_as_parquet_with_kms_key method of BreweryWritter can fail.
    
    Args:
        test_parquet_raw (str): The raw Parquet data for testing.
        test_s3_path (str): The S3 path for testing.
        test_kms_key (str): The KMS key for testing.
        partition_cols (list): The partition columns for testing.
    """
    test_s3_path = "bad_path"
    response = BreweryWritter(test_kms_key).write_df_to_s3_as_parquet_with_kms_key(test_parquet_raw, test_s3_path, partition_cols)

    assert response["StatusCode"] == 400

def test_write_json_to_s3_with_kms_key(
        test_json_raw: str, test_s3_path_for_json: str, test_kms_key: str
):
    """Test the write_json_to_s3_with_kms_key method of BreweryWritter.

    Args:
        test_json_raw (str): The raw JSON data for testing.
        test_s3_path_for_json (str): The S3 path for testing.
        test_kms_key (str): The KMS key for testing.
    """
    response = BreweryWritter(test_kms_key).write_json_to_s3_with_kms_key(test_json_raw, test_s3_path_for_json)

    assert response["StatusCode"] == 200

def test_write_json_to_s3_with_kms_key_must_fail(
        test_json_raw: str, test_s3_path_for_json: str
):
    """Test if the write_json_to_s3_with_kms_key method of BreweryWritter can fail.

    Args:
        test_json_raw (str): The raw JSON data for testing.
        test_s3_path_for_json (str): The S3 path for testing.
        test_kms_key (str): The KMS key for testing.
    """
    test_kms_key = "wrong_key"
    response = BreweryWritter(test_kms_key).write_json_to_s3_with_kms_key(test_json_raw, test_s3_path_for_json)

    assert response["StatusCode"] == 400
