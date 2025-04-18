"""Mock AWS Lambda function for testing purposes."""


def lambda_handler(event, context):
    """This function is the entry point for the AWS Lambda function.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (LambdaContext): The context object providing runtime information."""

    print(event)
    print(context)
