import boto3
import logging
from botocore.exceptions import ClientError


def upload_files(file_path, image_name=None):
    """
    Upload images to the S3 bucket

    file_pat is the file to be uploaded
    bucket is the name of the bucket to upload 
    image_name is the S3 object(image) name. If not specified then file_name is used
    returns "File successfully Uploaded" if successful
    """

    # If the image was not specified, use image_name
    if image_name is None:
        image_name = file_path

    # Upload the image
    s3_client = boto3.client('s3')
    bucket = "bucket-name"
    try:
        response = s3_client.upload_file(file_path, bucket, image_name)
    except ClientError as e:
        logging.error(e)
        return False
    print("File Successfully Uploaded")
