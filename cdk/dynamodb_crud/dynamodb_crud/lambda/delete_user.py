import json
import logging

from botocore.exceptions import ClientError

import layer.utils as utils
from layer.user_service import delete

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(json.dumps(event))

    path_parameters = event.get("pathParameters")
    user_id = path_parameters.get("id")

    try:
        if not user_id:
            api_response = utils.build_response(400, "Invalid request. User id missing in the path parameter")
            return api_response

        response = delete(user_id)
        if response is None:
            message = f"No user exists for the given user id : {user_id}"
            status_code = 400
        else:
            message = f"User {user_id} deleted successfully"
            status_code = 200

        api_response = utils.build_response(status_code, message)
        return api_response

    except ClientError as e:
        # Handle AWS-specific errors
        utils.handle_aws_error(e)

    except Exception as e:
        # Handle any other exceptions
        utils.handle_error(e)
