import boto3
import logging
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region=None):
    """Creating an S3 bucket

    The region is not included in this because it is already set in the /.aws/config file.
    The region for all resources is set to us-east-1.

    bucket_name: Is the name of the bucket to create
    on success: Statement indicating bucket successfully created is returned
    else: 
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return print("Creation not successful")
    return print("The bucket " + bucket_name + " has been created successfully.")
