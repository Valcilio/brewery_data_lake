"""Mock AWS Lambda function for testing purposes."""

import logging
import boto3


def get_logger(file_name: str) -> logging.Logger:
    """
    Returns a logger instance with the specified file name.

    Parameters:
    file_name (str): The name of the log file.

    Returns:
    logging.Logger: A logger instance with the specified file name.
    """

    handlers = [logging.StreamHandler()]

    logging.basicConfig(
        format="%(name)s || %(asctime)s || (%(levelname)s) || %(message)s",
        level=logging.INFO,
        handlers=handlers,
    )

    logger = logging.getLogger(file_name)
    logger.setLevel("INFO")

    return logger


def lambda_handler(event, context):
    """This function is the entry point for the AWS Lambda function.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (LambdaContext): The context object providing runtime information."""

    try:
        logger = get_logger(file_name="lambda_handler")
        logger.info(event)
        logger.info(context)
        if event["retry_number"] >= 4:
            logger.error("Max retry limit reached. Exiting process.")
            raise ValueError("Max retry limit reached. Exiting process.")
    except Exception as e:
        logger.error(f"Error in lambda_handler: {e}")
        boto3.client("sns").publish(
            TopicArn=f"arn:aws:sns:{event['aws_region']}:{event['account_id']}:brewery_etl_topic",
            Message=str(e),
        )
        raise e
