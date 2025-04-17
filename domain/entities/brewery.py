import pickle
import json

import pandas as pd
from pandas.testing import assert_series_equal

from domain.utils.etllogger import ETLLogger


class Brewery:

    def __init__(self, data: json):
        """Initialize the Brewery class.
        
        Args:
            data (pd.DataFrame): DataFrame containing brewery data.
        """
        self.data = pd.DataFrame(data)
        self.logger = ETLLogger("Timeseries").get_logger()

    def validate_dtypes(self):
        """Validate the dtypes of the dataframe.

        It checks if the dtypes of the dataframe match the expected dtypes."""

        self.logger.info("Validating dtypes of the dataframe.")
        assert_series_equal(self._load_correct_dtypes(), self.data.dtypes)

    def _load_correct_dtypes(self):
        """
        Load the correct dtypes from a pickle file."""
        return pickle.load(open("domain/artifacts/breweries_dtypes.pkl", "rb"))
