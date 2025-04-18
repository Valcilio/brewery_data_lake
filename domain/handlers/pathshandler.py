"""Module to handle paths for different file types."""

from datetime import datetime

from domain.utils.etllogger import ETLLogger


class PathsHandler:
    """A class to handle paths for different file types."""

    def __init__(self):
        """Initialize the PathsHandler class."""
        self.logger = ETLLogger("PathsHandler").get_logger()

    def define_path_for_parquet(self, bucket_name: str, key: str) -> str:
        """Define the path for parquet files."""

        self.logger.info(
            f"Defining path for parquet files in bucket: {bucket_name}, key: {key}"
        )
        return f"s3://{bucket_name}/{key}/{self._get_datetime_now()}"

    def define_path_for_json(self, bucket_name: str, key: str) -> str:
        """Define the path for json files."""
        self.logger.info(
            f"Defining path for json files in bucket: {bucket_name}, key: {key}"
        )
        return f"s3://{bucket_name}/{key}/{self._get_datetime_now()}.json"

    def _get_datetime_now(self) -> str:
        """Get the current date and time in a specific format.
        Returns:
            str: The current date and time in the format YYYY-MM-DD_HH:MM:SS.milliseconds.
        """

        self.logger.info("Getting current date and time with mileseconds granularity.")
        return datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
