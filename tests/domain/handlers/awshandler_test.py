"""Test the AWSHandler class."""

from domain.handlers.awshandler import AWSHandler


def test_invoke_lambda():
    """Test the get_secret method of S3Handler."""

    test_output = AWSHandler().get_secret(secret_name="API_KEYS")

    assert isinstance(test_output, dict)
