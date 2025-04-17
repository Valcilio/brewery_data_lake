import ast

import boto3

from domain.utils.etllogger import ETLLogger


class AWSHandler:

    def __init__(self):

        self.logger = ETLLogger(__name__).get_logger()
        self._secretsmanager_client()

    def get_secret(self, secret_name: str) -> dict:
        """Retrieves a secret from AWS Secrets Manager.

        Args:
            secret_name (str): The name of the secret to retrieve."""

        return ast.literal_eval(
            self.secretsmanager.get_secret_value(SecretId=secret_name)["SecretString"]
        )

    def _secretsmanager_client(self):
        """
        Initializes the S3 client.

        Returns:
            boto3.client: The S3 client.
        """
        self.logger.info("Initializing SecretsManager client")
        self.secretsmanager = boto3.client("secretsmanager")
