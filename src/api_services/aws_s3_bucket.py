import os
import boto3
from src.api_services.credentials import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_S3_BUCKET_NAME
from src.utility.local_loger import logger


def upload_audio_file_to_s3(local_file_path, s3_file_name):
    """
    This function is used to upload an audio file to an S3 bucket.

    Args:
        local_file_path (str): Path to the local audio file.
        s3_file_name (str): Name of the audio file in the S3 bucket.

    Returns:
        bool: Returns True if the file is uploaded successfully, else False.
    """
    try:
        s3_client = boto3.client(
            service_name='s3',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        response = s3_client.upload_file(local_file_path, AWS_S3_BUCKET_NAME, s3_file_name)
        return True
    except Exception as e:
        print(f"Error occured during uploading file to S3. {e.__str__()}")
        return False


def get_latest_file_upload():
    s3_client = boto3.client(
            service_name='s3',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
    objs = s3_client.list_objects_v2(Bucket=AWS_S3_BUCKET_NAME, Delimiter='/') ['Contents']
    print(objs)
    objs.sort(key=lambda e: e['LastModified'], reverse=True)
    print("******")
    print(objs[0])
    first_item = list(objs[0].items())[0]
    logger.info(f"First file at bucket: {first_item[1]}")
    return first_item[1]

