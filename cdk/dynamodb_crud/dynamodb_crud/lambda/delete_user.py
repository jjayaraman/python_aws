import json

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Users")


def lambda_handler(event, context):
    print(json.dumps(event))

    path_parameters = event.get("pathParameters")
    user_id = path_parameters.get("id")

    try:
        if not user_id:
            return {
                "statusCode": 400,
                "body": "Invalid request. User id missing in the path parameter"
            }
        key = {"user_id": user_id}

        response = table.delete_item(Key=key)

        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }

    except Exception as e:
        print(f"Error occurred in delete_user lambda is: {str(e)}")
        return {
            "statusCode": 500,
            "body": {"error": f"An unexpected error occurred: {str(e)}"}
        }
