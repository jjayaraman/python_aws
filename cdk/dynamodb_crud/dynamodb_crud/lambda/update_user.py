"""
Python Lambda to update a record in DynamoDB using update_item
"""

import json

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')


def lambda_handler(event, context):
    print('update_user lambda event:', json.dumps(event))

    # Get user_id from path parameters
    path_parameters = event.get("pathParameters")
    user_id = path_parameters.get("id")

    # Get API payload from body
    user_str = event.get('body')

    try:
        if not user_id:
            return {
                "statusCode": 400,
                "body": "Missing 'id' path parameter"
            }

        if not user_str:
            return {
                "statusCode": 400,
                "body": "Missing 'id' path parameter"
            }

        user = json.loads(user_str)

        first_name = user["first_name"]
        last_name = user["last_name"]

        partition_key = {"user_id": user_id}
        update_expression = "SET #first_name = :first_name, #last_name = :last_name"
        expression_attribute_names = {"#first_name": "first_name", "#last_name": "last_name"}
        expression_attribute_values = {":first_name": first_name, ":last_name": last_name}

        response = table.update_item(Key=partition_key, UpdateExpression=update_expression,
                                     ExpressionAttributeNames=expression_attribute_names,
                                     ExpressionAttributeValues=expression_attribute_values,
                                     ReturnValues="UPDATED_NEW"
                                     )
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }

    except Exception as e:
        # Handle any exceptions
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"An unexpected error occurred: {str(e)}"})
        }
