import json
import awswrangler as wr

from pandas import DataFrame

from domain.utils.etllogger import ETLLogger


class BreweryWritter:
    """Module for writting brewery data into an S3 bucket."""

    def __init__(self, kms_key: str):
        """Initialize the BreweryLoader class.

        Args:
            kms_key (str): The KMS key for S3 encryption.
        """

        self.kms_key = kms_key
        self.logger = ETLLogger("BreweryWriter").get_logger()

    def write_df_to_s3_as_parquet_with_kms_key(self, df: DataFrame, s3_path: str, partition_cols: list) -> dict:
        """Load the DataFrame into an S3 bucket."""

        try:
            self.logger.info("Configurating KMS key to put data into S3 encrypted.")
            extra_args = {
                "ServerSideEncryption": "aws:kms",
                "SSEKMSKeyId": self.kms_key,
            }

            self.logger.info("Writting data into S3 bucket.")
            wr.s3.to_parquet(df=df, path=s3_path, partition_cols=partition_cols, s3_additional_kwargs=extra_args, dataset=True)
            self.logger.info("Data written successfully.")
            return {"Body": "Data loaded successfully", "StatusCode": 200}
        except Exception as e:
            msg = f"Error writing data to S3: {e}"
            self.logger.error(msg)
            return {"Body": msg, "StatusCode": 400}

    def write_json_to_s3_with_kms_key(self, data: list, s3_path: str) -> dict:
        """Load the JSON data into an S3 bucket."""

        try:
            self.logger.info("Configurating KMS key to put data into S3 encrypted.")
            extra_args = {
                "ServerSideEncryption": "aws:kms",
                "SSEKMSKeyId": self.kms_key,
            }

            self.logger.info("Writting data into S3 bucket.")
            wr.s3.to_json(DataFrame(data), path=s3_path, s3_additional_kwargs=extra_args)
            self.logger.info("Data written successfully.")
            return {"Body": "Data loaded successfully", "StatusCode": 200}
        except Exception as e:
            msg = f"Error writing data to S3: {e}"
            self.logger.error(msg)
            return {"Body": msg, "StatusCode": 400}