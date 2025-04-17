"""Module to define fixtures for testing the domain layer of the application."""

import os
import pickle

from pandas import read_parquet
import pytest

@pytest.fixture
def partition_cols():
    """Fixture to provide partition columns for testing."""
    return ["brewery_type", "country", "state_province", "city"]

@pytest.fixture
def test_kms_key():
    """Fixture to provide a KMS key for testing."""
    return os.environ["KMS_KEY"]

@pytest.fixture
def test_json_raw():
    """Fixture to load raw JSON data for testing."""
    return pickle.load(open("tests/test_data/breweries_test_json.pkl", "rb"))

@pytest.fixture
def test_s3_path():
    """Fixture to provide an S3 path for testing."""
    return "s3://brewery-test-files-temp/test-data/test_brewery_parquet"

@pytest.fixture
def test_s3_path_for_json():
    """Fixture to provide an S3 path for testing."""
    return "s3://brewery-test-files-temp/test-data/test_brewery_data.json"

@pytest.fixture
def test_parquet_raw():
    """Fixture to load raw Parquet data for testing."""
    return read_parquet("tests/test_data/test_parquet_raw.parquet")


@pytest.fixture
def test_url():
    """Fixture to provide a URL for testing."""
    return "https://api.openbrewerydb.org/v1/breweries?page=1"


@pytest.fixture
def test_wrong_url():
    """Fixture to provide a wrong URL for testing."""
    return "https://wrongurl.com/breweries.json"
