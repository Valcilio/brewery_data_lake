"""Module to handle the raw data."""

from pandas import DataFrame

from domain.usecases.breweryextractor import BreweryExtractor
from domain.usecases.brewerytransformer import BreweryTransformer
from domain.usecases.brewerywritter import BreweryWritter
from domain.utils.etllogger import ETLLogger


class DataHandler:
    """Handler class for managing brewery data extraction and transformation."""

    def __init__(self, kms_key: str):
        """Initialize the BreweryAPIHandler class.
        Args:
            url (str): The URL to extract data from.
            s3_path (str): The S3 path to store the data.
            kms_key (str): The KMS key for encryption.
        """
        
        self.kms_key = kms_key
        self.logger = ETLLogger("BreweryAPIHandler").get_logger()

    def handle_raw_data(self, s3_path: str, start_page: str):
        """Handle raw data controlling it extraction and write."""

        url = (
            f"https://api.openbrewerydb.org/v1/breweries?page={start_page}&per_page=200"
        )
        raw_data = BreweryExtractor(url).extract_data()
        if raw_data["StatusCode"] == 200:
            return BreweryWritter(self.kms_key).write_json_to_s3_with_kms_key(
                raw_data["Body"], s3_path
            )

        return raw_data
    
    def handle_processed_data(self, s3_path: str, raw_data: str):
        """Handle the processed data to the save it inside the silver layer."""

        silver_df = BreweryTransformer().structure_into_dataframe(raw_data)
        return BreweryWritter(self.kms_key).write_df_to_s3_as_parquet_with_kms_key(
                silver_df, s3_path, ["brewery_location"]
            )
    
    def handle_view_data(self, s3_path: str, silver_df: DataFrame):
        """Handle the data created for the view which will be saved at the gold layer."""

        gold_df = BreweryTransformer().get_brewery_quantity_aggregated_by_location_and_type(silver_df)
        return BreweryWritter(self.kms_key).write_df_to_s3_as_parquet_with_kms_key(
            gold_df, s3_path, ["brewery_type"]
        )

