"""Test module for testing the data handler."""

from pandas import DataFrame

from domain.handlers.datahandler import DataHandler


def test_handle_raw_data(
    test_start_page: str, test_s3_path_for_raw_data_handler: str, test_kms_key: str
):
    """Test if the handle raw data is able to handler the raw data."""

    output = DataHandler(
        test_kms_key
    ).handle_raw_data(test_s3_path_for_raw_data_handler, test_start_page)

    assert output["StatusCode"] == 200

def test_handle_processed_data(
    test_parquet_without_brewery_loc: DataFrame, test_s3_path_for_raw_data_handler: str, test_kms_key: str
):
    """Test if the handle processed data is able to handler the processed data."""

    output = DataHandler(
        test_kms_key
    ).handle_processed_data(test_s3_path_for_raw_data_handler, test_parquet_without_brewery_loc)

    assert output["StatusCode"] == 200

def test_handle_processed_data(
    test_parquet_with_brewery_loc: DataFrame, test_s3_path_for_raw_data_handler: str, test_kms_key: str
):
    """Test if the handle processed data is able to handler the processed data."""

    output = DataHandler(
        test_kms_key
    ).handle_processed_data(test_s3_path_for_raw_data_handler, test_parquet_with_brewery_loc)

    assert output["StatusCode"] == 200