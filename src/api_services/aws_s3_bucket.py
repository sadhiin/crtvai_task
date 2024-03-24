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


def get_bucket_latest_file_upload():
  """
  Retrieves the URL of the latest uploaded file from an S3 bucket.

  Returns:
      str: The URL of the latest file in the S3 bucket, or None if an error occurs.
  """
  try:
    s3_client = boto3.client(
        service_name='s3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # Get object listing for the bucket (excluding common prefixes)
    response = s3_client.list_objects_v2(Bucket=AWS_S3_BUCKET_NAME)
    contents = response.get('Contents', [])  # Handle empty bucket case

    # Sort objects by LastModified in descending order (latest first)
    contents.sort(key=lambda obj: obj.get('LastModified'), reverse=True)

    # Check if any files were found
    if not contents:
      logger.info(f"No files found in bucket: {AWS_S3_BUCKET_NAME}")
      return None

    # Get the key (filename) of the latest object
    latest_file_key = contents[0]['Key']

    # Construct the S3 object URL
    s3_object_url = f"s3://{AWS_S3_BUCKET_NAME}/{latest_file_key}"

    logger.info(f"Latest file URL: {s3_object_url}")
    return s3_object_url

  except Exception as e:
    logger.error(f"Error occured during getting latest file from S3. {e.__str__()}")
    return None