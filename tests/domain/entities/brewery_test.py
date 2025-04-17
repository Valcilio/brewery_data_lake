"""Test the Brewery class."""

from domain.entities.brewery import Brewery


def test_validate_dtypes(test_json_raw: list):
    """Test the validate_dtypes method of the Timeseries class."""

    Brewery(test_json_raw).validate_dtypes()
