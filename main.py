"""Main ETL process for the Brewery data pipeline."""

import os

from domain.handlers.awshandler import AWSHandler
from domain.handlers.datahandler import DataHandler
from domain.handlers.pathshandler import PathsHandler
from domain.utils.etllogger import ETLLogger

LOGGER = ETLLogger("ETLProcess").get_logger()


def main():
    """Main function to run the ETL process."""

    event = get_event()
    bronze_data_path, silver_data_path, gold_data_path = get_paths(event)

    data_handler = DataHandler(event["kms_key"])
    LOGGER.info("Starting the handling of the bronze data.")
    bronze_output = data_handler.handle_raw_data(bronze_data_path, event["start_page"])
    if bronze_output["StatusCode"] == 200:
        LOGGER.info("Bronze data written successfully.")
        LOGGER.info("Starting the handling of the silver data.")
        silver_output = data_handler.handle_processed_data(
            silver_data_path, bronze_output["Body"]
        )
        if silver_output["StatusCode"] == 200:
            LOGGER.info("Silver data written successfully.")
            LOGGER.info("Starting the handling of the gold data.")
            gold_output = data_handler.handle_view_data(
                gold_data_path, silver_output["Body"]
            )
            if gold_output["StatusCode"] == 200:
                LOGGER.info("Gold data written successfully.")
                AWSHandler().put_parameter(
                    parameter_name=os.environ["START_PAGE_PARAMETER_NAME"],
                    value=str(int(event["start_page"]) + 4),
                )
                LOGGER.info("Process finished successfully.")
                return {"StatusCode": 200}

    LOGGER.error("Error in this process!")
    send_error_with_sns(
        "Error in the Brewery ETL process, please, check the logs in cloudwatch to debug it!",
        event,
    )
    retry_process(event)

    return {"StatusCode": 400}


def get_paths(event: dict):
    """Get the paths for bronze, silver, and gold data layers.

    Args:
        event (dict): The event dictionary containing the S3 bucket and key information.
    """

    bronze_data_path = PathsHandler().define_path_for_json(
        event["bronze_bucket"], event["bronze_key"]
    )
    silver_data_path = PathsHandler().define_path_for_parquet(
        event["silver_bucket"], event["silver_key"]
    )
    gold_data_path = PathsHandler().define_path_for_parquet(
        event["gold_bucket"], event["gold_key"]
    )

    return bronze_data_path, silver_data_path, gold_data_path


def send_error_with_sns(error_message: str, event: dict):
    """Send an error message to SNS topic.

    Args:
        error_message (str): The error message to send.
        event (dict): The event dictionary containing the AWS region and account ID."""

    AWSHandler().publish_message_to_sns(
        topic_arn=f"arn:aws:sns:{event['aws_region']}:{event['account_id']}:brewery_test_topic",
        message=error_message,
    )


def retry_process(event: dict):
    """Retry the ETL process by invoking the Lambda function again.
    Args:
        event (dict): The event dictionary containing the Lambda function name and retry number.
    """

    retry_number = int(event["retry_number"])
    event["retry_number"] = str(retry_number + 1)
    AWSHandler().invoke_lambda(
        lambda_name=event["lambda_name"], retry_number=retry_number + 1, event=event
    )


def get_event() -> dict:
    """Get the event dictionary with environment variables.
    Returns:
        dict: The event dictionary containing the environment variables.
    """

    event = {
        "kms_key": os.environ["KMS_KEY"],
        "start_page": AWSHandler().retriever_parameter(
            parameter_name=os.environ["START_PAGE_PARAMETER_NAME"]
        )["Parameter"]["Value"],
        "bronze_bucket": os.environ["BRONZE_BUCKET"],
        "silver_bucket": os.environ["SILVER_BUCKET"],
        "gold_bucket": os.environ["GOLD_BUCKET"],
        "bronze_key": os.environ["BRONZE_KEY"],
        "silver_key": os.environ["SILVER_KEY"],
        "gold_key": os.environ["GOLD_KEY"],
        "aws_region": os.environ["AWS_REGION"],
        "aws_account_id": os.environ["AWS_ACCOUNT_ID"],
        "retry_number": os.environ["RETRY_NUMBER"],
        "lambda_name": os.environ["LAMBDA_NAME"],
    }

    return event


if __name__ == "__main__":
    main()
