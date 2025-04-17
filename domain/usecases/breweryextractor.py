"""Module for extracting brewery data from a given URL."""

import requests

from domain.entities.brewery import Brewery
from domain.utils.etllogger import ETLLogger


class BreweryExtractor:
    """Extractor class for fetching brewery data from a specified URL."""

    def __init__(self, url: str):
        """Initialize the BreweryExtractor class.
        Args:
            url (str): The URL to extract data from.
        """
        self.url = url
        self.logger = ETLLogger("BreweryExtractor").get_logger()

    def extract_data(self) -> dict:
        """Extract data from the given URL."""
        try:
            self.logger.info(f"Extracting data from {self.url}.")
            json_response = requests.get(self.url, timeout=180).json()
            dtypes_check_result = self._check_dtypes(json_response)
            if dtypes_check_result["StatusCode"] == 400:
                return dtypes_check_result
            self.logger.info("Extraction completed successfully.")
            return {"Body": json_response, "StatusCode": 200}
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching data from {self.url}: {e}")
            return {"Body": f"Error fetching data from {self.url}", "StatusCode": 400}

    def _check_dtypes(self, json_response: list):
        """Check the dtypes of the extracted data."""
        try:
            Brewery(json_response).validate_dtypes()
            return {"Body": "Dtypes match", "StatusCode": 200}
        except AssertionError:
            self.logger.error("Data validation failed. Dtypes do not match.")
            return {"Body": "Data validation failed", "StatusCode": 400}
