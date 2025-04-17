import json

import pandas as pd

from domain.entities.brewery import Brewery


def test_validate_dtypes(test_json_raw: json):
    """Test the validate_dtypes method of the Timeseries class."""

    Brewery(test_json_raw).validate_dtypes()
