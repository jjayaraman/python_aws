import io
import json
import logging
import os
import zipfile

import boto3
from botocore.exceptions import ClientError

import layer.utils as utils

s3_client = boto3.client('s3')

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

destination_s3_bucket = os.getenv("destination_s3_bucket")


def handler(event, context):
    logger.debug(json.dumps(event, indent=2))
    logger.debug(f"destination_s3_bucket : {destination_s3_bucket}")
    try:

        # Retrieve bucket and object details from the event
        for record in event['Records']:
            source_bucket_name = record['s3']['bucket']['name']
            zip_key = record['s3']['object']['key']
            logger.debug(f"source_bucket_name {source_bucket_name} zip_key {zip_key}")

            # Download the zip file from S3
            if zip_key.endswith('.zip'):
                zip_obj = s3_client.get_object(Bucket=source_bucket_name, Key=zip_key)
                buffer = io.BytesIO(zip_obj['Body'].read())

                zip_filename = os.path.splitext(os.path.basename(zip_key))[0]
                folder_prefix = f"{zip_filename}/"

                with zipfile.ZipFile(buffer) as zip_ref:
                    for file_info in zip_ref.infolist():
                        if not file_info.is_dir():
                            file_data = zip_ref.read(file_info.filename)
                            target_key = f"{folder_prefix}{file_info.filename}"

                            # Upload extracted file back to S3
                            s3_client.put_object(Bucket=destination_s3_bucket, Key=target_key, Body=file_data)
                            logger.debug(f"Extracted and uploaded: {target_key}")

                # Delete zip file in source bucket
                s3_client.delete_object(Bucket=source_bucket_name, Key=zip_key)
                logger.debug(f"File {zip_key} deleted from bucket {source_bucket_name}")

            else:
                logger.debug(f"Skipped non-zip file: {zip_key}")

    except json.JSONDecodeError as e:
        # Handle JSON errors
        utils.handle_json_decode_error(e)

    except ClientError as e:
        # Handle AWS-specific errors
        utils.handle_aws_error(e)

    except Exception as e:
        # Handle any other exceptions
        utils.handle_error(e)
