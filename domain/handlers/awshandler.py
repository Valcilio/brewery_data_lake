"""Module for handling AWS services."""

import json

import boto3

from domain.utils.etllogger import ETLLogger


class AWSHandler:
    """Handles AWS services."""

    def __init__(self):

        self.logger = ETLLogger(__name__).get_logger()
        self._lambda_client()

    def invoke_lambda(self, lambda_name: str, retry_number: int, event: dict) -> dict:
        """Retrieves a secret from AWS Secrets Manager.

        Args:
            secret_name (str): The name of the secret to retrieve."""

        self.logger.info(f"Invoking lambda for retry number {retry_number}")
        self.lambda_client.invoke(FunctionName=lambda_name, LogType='Tail', Payload=json.dumps({event}))
        

    def _lambda_client(self):
        """
        Initializes the S3 client.

        Returns:
            boto3.client: The S3 client.
        """
        self.logger.info("Initializing Lambda Function client")
        self.lambda_client = boto3.client("lambda")
