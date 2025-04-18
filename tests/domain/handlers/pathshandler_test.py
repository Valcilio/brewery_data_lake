"""Test the PathsHandler class."""

import re

from domain.handlers.pathshandler import PathsHandler


def test_define_path_for_parquet(test_bucket_name: str, test_bucket_key: str):
    """Test the define_path_for_parquet method."""
    parquet_path = PathsHandler().define_path_for_parquet(
        test_bucket_name, test_bucket_key
    )

    assert re.match(
        r"^s3:\/\/([^\/]+)\/([^\/]+)\/(.+)$",
        parquet_path,
    )


def test_define_path_for_json(test_bucket_name: str, test_bucket_key: str):
    """Test the define_path_for_json method."""
    json_path = PathsHandler().define_path_for_json(test_bucket_name, test_bucket_key)

    assert re.match(
        r"^s3:\/\/([^\/]+)\/([^\/]+)\/(.+\.json)$",
        json_path,
    )
