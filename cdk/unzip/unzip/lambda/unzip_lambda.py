import boto3
import zipfile
import io
import os
import json


def handler(event, context):
    print(f"event {json.dumps(event)}")
    s3_client = boto3.client('s3')

    # Retrieve bucket and object details from the event
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        zip_key = record['s3']['object']['key']
        print(f"bucket_name {bucket_name} zip_key {zip_key}")

        # Download the zip file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=zip_key)
        if zip_key.endswith('.zip'):
            zip_obj = s3_client.get_object(Bucket=bucket_name, Key=zip_key)
            buffer = io.BytesIO(zip_obj['Body'].read())

            zip_filename = os.path.splitext(os.path.basename(zip_key))[0]
            folder_prefix = f"{zip_filename}/"

            with zipfile.ZipFile(buffer) as zip_ref:
                for file_info in zip_ref.infolist():
                    if not file_info.is_dir():
                        file_data = zip_ref.read(file_info.filename)
                        target_key = f"{folder_prefix}{file_info.filename}"

                        # Upload extracted file back to S3
                        s3_client.put_object(Bucket=bucket_name, Key=target_key, Body=file_data)
                        print(f"Extracted and uploaded: {target_key}")
        else:
            print(f"Skipped non-zip file: {zip_key}")
