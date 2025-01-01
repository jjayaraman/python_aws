import json
import logging

from botocore.exceptions import ClientError

import layer.utils as utils
from layer.user_service import search_users

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:

        logger.info(f"search_users lambda event: {json.dumps(event, indent=2)}")

        params = event.get("queryStringParameters", {})
        logger.debug(f"params: {params}")

        first_name = params.get("first_name", None)
        last_name = params.get("last_name", None)

        response = search_users(first_name, last_name)
        logger.debug(f"response: {response}")

        if response.get("Items"):
            users = response.get("Items")
            api_response = utils.build_response(200, json.dumps(users))
        else:
            api_response = utils.build_response(400, "No data found")

        return api_response

    except ClientError as ae:
        utils.handle_aws_error(ae)

    except Exception as e:
        utils.handle_error(e)
