"""Module for handling AWS services."""

import json

import boto3

from domain.utils.etllogger import ETLLogger


class AWSHandler:
    """Handles AWS services."""

    def __init__(self):

        self.logger = ETLLogger(__name__).get_logger()

    def invoke_lambda(self, lambda_name: str, retry_number: int, event: dict) -> dict:
        """Retrieves a secret from AWS Secrets Manager.

        Args:
            secret_name (str): The name of the secret to retrieve."""

        lambda_client = self._lambda_client()
        self.logger.info(f"Invoking lambda for retry number {retry_number}")
        return lambda_client.invoke(
            FunctionName=lambda_name, LogType="Tail", Payload=json.dumps(event)
        )

    def publish_message_to_sns(self, topic_arn: str, message: str) -> dict:
        """Publishes a message to an SNS topic.

        Args:
            topic_arn (str): The ARN of the SNS topic.
            message (str): The message to publish.

        Returns:
            dict: The response from the SNS publish operation.
        """
        sns_client = self._sns_client()
        self.logger.info(f"Publishing message to SNS topic {topic_arn}")
        return sns_client.publish(TopicArn=topic_arn, Message=message)

    def retriever_parameter(self, parameter_name: str):
        """Retrieves a parameter from AWS Systems Manager Parameter Store.

        Args:
            parameter_name (str): The name of the parameter to retrieve.

        Returns:
            dict: The response from the SSM get_parameter operation.
        """
        try:
            ssm_client = self._ssm_client()
            self.logger.info(f"Retrieving parameter {parameter_name} from SSM")
            return ssm_client.get_parameter(Name=parameter_name)
        except ssm_client.exceptions.ParameterNotFound:
            self.put_parameter(
                parameter_name=parameter_name, value="1"
            )

    def put_parameter(self, parameter_name: str, value: str):
        """Puts a parameter into AWS Systems Manager Parameter Store.

        Args:
            parameter_name (str): The name of the parameter to put.
            value (str): The value of the parameter.

        Returns:
            dict: The response from the SSM put_parameter operation.
        """
        ssm_client = self._ssm_client()
        self.logger.info(
            f"Putting parameter {parameter_name} with value {value} into SSM"
        )
        return ssm_client.put_parameter(
            Name=parameter_name, Value=value, Type="String", Overwrite=True
        )

    def _lambda_client(self):
        """
        Initializes the Lambda client.

        Returns:
            boto3.client: The Lambda client.
        """
        self.logger.info("Initializing Lambda Function client")
        return boto3.client("lambda", region_name="us-east-1")

    def _sns_client(self):
        """
        Initializes the SNS client.

        Returns:
            boto3.client: The SNS client.
        """
        self.logger.info("Initializing SNS client")
        return boto3.client("sns", region_name="us-east-1")

    def _ssm_client(self):
        """
        Initializes the SSM client.

        Returns:
            boto3.client: The SSM client.
        """
        self.logger.info("Initializing SSM client")
        return boto3.client("ssm", region_name="us-east-1")
