"""
Python Lambda to create a record in DynamoDB using put_item
"""

import json

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Users")


def lambda_handler(event, context):
    print(json.dumps(event, indent=2))
    try:

        user_str = event.get("body")
        if not user_str:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing request body"})
            }
        user = json.loads(user_str)
        table.put_item(Item=user)
        return {
            "statusCode": 200,
            "body": f"User created: {user_str}"
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
