"""
Python Lambda to get records from DynamoDB using scan
"""

import json
import logging

from botocore.exceptions import ClientError

import layer.utils as utils
from layer.user_service import get_users

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.debug(json.dumps(event))
    try:
        response = get_users()
        users = response.get('Items', [])

        api_response = utils.build_response(200, json.dumps({'users': users}))
        return api_response

    except ClientError as e:
        # Handle AWS-specific errors
        utils.handle_aws_error(e)

    except Exception as e:
        # Handle any other exceptions
        utils.handle_error(e)
