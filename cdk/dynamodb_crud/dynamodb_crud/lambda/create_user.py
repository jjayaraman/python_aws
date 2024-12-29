import json

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("users")


def lambda_handler(event, context):
    print(json.dumps(event, indent=2))
    first_name = event["first_name"]
    last_name = event["last_name"]

    user = {
        "first_name": first_name,
        "last_name": last_name
    }

    try:
        table.put_item(Item=user)
        return {
            "statusCode": 200,
            "body": "User created "
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
