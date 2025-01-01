"""
Python Lambda to create a record in DynamoDB using put_item
"""

import json
import logging

from botocore.exceptions import ClientError

import layer.utils as utils
from layer.user_service import create

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.debug(json.dumps(event, indent=2))
    try:

        user_str = event.get("body")
        if not user_str:
            api_response = utils.build_response(400, json.dumps({"error": "Missing request body"}))
            return api_response

        user = json.loads(user_str)
        response = create(user)
        logger.debug(f"User create response: {response}")

        api_response = utils.build_response(200, f"User create successfully")
        return api_response

    except json.JSONDecodeError as e:
        # Handle JSON errors
        utils.handle_json_decode_error(e)

    except ClientError as e:
        # Handle AWS-specific errors
        utils.handle_aws_error(e)

    except Exception as e:
        # Handle any other exceptions
        utils.handle_error(e)
