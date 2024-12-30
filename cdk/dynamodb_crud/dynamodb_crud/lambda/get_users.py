"""
Python Lambda to get records from DynamoDB using scan
"""

import json

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')


def lambda_handler(event, context):
    print(json.dumps(event))
    try:
        response = table.scan()
        users = response.get('Items', [])

        return {
            "statusCode": 200,
            "body": json.dumps({'users': users})
        }

    except ClientError as e:
        # Handle AWS-specific errors
        error_message = e.response['Error']['Message']
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"AWS ClientError: {error_message}"})
        }

    except Exception as e:
        # Handle any other exceptions
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"An unexpected error occurred: {str(e)}"})
        }
