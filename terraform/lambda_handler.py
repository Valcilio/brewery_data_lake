"""Mock AWS Lambda function for testing purposes."""

import os
import logging
import json

import boto3


def lambda_handler(event, context):
    """This function is the entry point for the AWS Lambda function.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (LambdaContext): The context object providing runtime information."""

    try:
        logger = get_logger(file_name="lambda_handler")
        logger.info(event)
        logger.info(context)
        if int(event["RETRY_NUMBER"]) >= 4:
            logger.error("Max retry limit reached. Exiting process.")
            raise ValueError("Max retry limit reached. Exiting process.")
        logger.info("Creating EC2 instance for ETL process.")
        output = create_ec2_for_etl(event=event)
        logger.info("EC2 instance created successfully.")
        return output
    except Exception as e:
        logger.error(f"Error in lambda_handler: {e}")
        boto3.client("sns").publish(
            TopicArn=f"arn:aws:sns:{event['AWS_REGION']}:{event['AWS_ACCOUNT_ID']}:brewery_etl_topic",
            Message=str(e),
            Subject="Brewery ETL Lambda Error",
        )
        raise e


def create_ec2_for_etl(event: dict) -> boto3.resource:
    """
    Create a EC2 machine for the ETL.

    Args:
        event (dict): the event with the request data.
        context (dict): the context with the context
        (like the moment of the request and from where the request came) data.
    """

    ec2 = boto3.resource("ec2", region_name="us-east-1")
    ecr_image = f"{os.environ['ECR_IMAGE_NAME']}:{os.environ['ECR_IMAGE_TAG']}"
    account_number = event["AWS_ACCOUNT_ID"]

    instance = ec2.create_instances(
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/xvda",
                "VirtualName": "brewery-etl",
                "Ebs": {
                    "DeleteOnTermination": True,
                    "VolumeSize": 30,
                    "VolumeType": "standard",
                },
            }
        ],
        ImageId="ami-053a45fff0a704a47",
        InstanceType="c6a.2xlarge",
        MaxCount=1,
        MinCount=1,
        Monitoring={"Enabled": True},
        UserData=f"""#!/bin/bash
 
echo "Installing Docker"
sudo yum install -y docker
systemctl start docker
systemctl status docker
 
echo "Assuming EC2 Role"
aws sts get-caller-identity
 
echo "Logging in Docker and ECR"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {account_number}.dkr.ecr.us-east-1.amazonaws.com
 
echo "Starting Docker Pulling"
docker pull {account_number}.dkr.ecr.us-east-1.amazonaws.com/{ecr_image}
docker run \
  -v "$HOME/.aws:/root/.aws" \
  -e KMS_KEY={event["KMS_KEY"]} \
  -e START_PAGE_PARAMETER_NAME={event["START_PAGE_PARAMETER_NAME"]} \
  -e BRONZE_BUCKET={event["BRONZE_BUCKET"]} \
  -e SILVER_BUCKET={event["SILVER_BUCKET"]} \
  -e GOLD_BUCKET={event["GOLD_BUCKET"]} \
  -e BRONZE_KEY={event["BRONZE_KEY"]} \
  -e SILVER_KEY={event["SILVER_KEY"]} \
  -e GOLD_KEY={event["GOLD_KEY"]} \
  -e AWS_REGION={event["AWS_REGION"]} \
  -e AWS_DEFAULT_REGION={event["AWS_REGION"]} \
  -e AWS_ACCOUNT_ID={event["AWS_ACCOUNT_ID"]} \
  -e RETRY_NUMBER={event["RETRY_NUMBER"]} \
  -e LAMBDA_NAME={event["LAMBDA_NAME"]} \
    {account_number}.dkr.ecr.us-east-1.amazonaws.com/{ecr_image}
 
echo "Starting the shutdown"
shutdown -h now""",
        DisableApiTermination=False,
        IamInstanceProfile={"Name": os.environ["EC2_INSTANCE_PROFILE"]},
        InstanceInitiatedShutdownBehavior="terminate",
        DisableApiStop=False,
    )

    return json.loads(json.dumps(instance, default=str))


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
