import json


def lambda_handler(event, context):
    print(json.dumps(event, indent=2))
    return {
        "statusCode": 200,
        "body": 'Hello World!'
    }
