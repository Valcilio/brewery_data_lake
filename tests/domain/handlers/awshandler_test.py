"""Test the AWSHandler class."""

import os

from domain.handlers.awshandler import AWSHandler


def test_invoke_lambda():
    """Test if the invoke_lambda method of AWSHandler works correctly."""

    test_output = AWSHandler().invoke_lambda(
        lambda_name="brewery_test_lambda",
        retry_number=1,
        event={"test_value": "this_is_a_test"},
    )

    assert test_output["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_publish_message_to_sns():
    """Test if the publish_message_to_sns method of AWSHandler works correctly."""

    aws_region = os.environ["AWS_DEFAULT_REGION"]
    account_id = os.environ["AWS_ACCOUNT_ID"]
    test_output = AWSHandler().publish_message_to_sns(
        topic_arn=f"arn:aws:sns:{aws_region}:{account_id}:brewery_test_topic",
        message="this_is_a_test",
    )

    assert test_output["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_put_parameter(test_parameter_name: str):
    """Test the put_parameter method of AWSHandler."""

    test_output = AWSHandler().put_parameter(
        parameter_name=test_parameter_name, value="1"
    )

    assert test_output["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_retriever_parameter(test_parameter_name: str):
    """Test the retriever_parameter method of AWSHandler."""

    test_output = AWSHandler().retriever_parameter(parameter_name=test_parameter_name)

    assert test_output["Parameter"]["Value"] == "1"
