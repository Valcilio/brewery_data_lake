"""Test the BreweryExtractor class."""

from domain.usecases.breweryextractor import BreweryExtractor


def test_extract_data_must_sucess(test_url: str):
    """Test the successful extraction of data from a valid URL."""

    test_json = BreweryExtractor(test_url).extract_data()

    assert test_json["StatusCode"] == 200


def test_extract_data_must_fail(test_wrong_url: str):
    """Test the failure of data extraction from an invalid URL."""

    test_json = BreweryExtractor(test_wrong_url).extract_data()

    assert test_json["StatusCode"] == 400
