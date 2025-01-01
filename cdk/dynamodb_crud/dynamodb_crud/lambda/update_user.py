"""
Python Lambda to update a record in DynamoDB using update_item
"""

import json
import logging

from botocore.exceptions import ClientError

import layer.utils as utils
from layer.user_service import update

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.debug('update_user lambda event:', json.dumps(event))

    # Get user_id from path parameters
    path_parameters = event.get("pathParameters")
    user_id = path_parameters.get("id")
    timestamp = path_parameters.get("timestamp")

    # Get API payload from body
    user_str = event.get('body')

    try:
        if not user_id:
            api_response = utils.build_response(400, "Invalid request. User id missing in the path parameter")
            return api_response

        if not user_str:
            api_response = utils.build_response(400, "Invalid request. User payload missing in body")
            return api_response

        user = json.loads(user_str)

        first_name = user["first_name"]
        last_name = user["last_name"]
        # timestamp = user["timestamp"]
        response = update(user_id, timestamp, first_name, last_name)
        logger.debug(f"response: {response}")

        api_response = utils.build_response(200, "User updated successfully")
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

    finally:
        logger.debug('All done')
