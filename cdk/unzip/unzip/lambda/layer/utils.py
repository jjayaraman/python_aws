"""
Helper utils for reusable common functions
"""

import json
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def build_response(status_code: int, message: str) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "body": message
    }


def handle_json_decode_error(e):
    logger.error(f"Invalid JSON format: {str(e)}")
    return build_response(400, json.dumps({"error": "Invalid JSON format in request body"}))


def handle_error(e):
    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    return build_response(500, "An unexpected error occurred")


def handle_aws_error(e):
    logger.error(f"AWS ClientError: {str(e)}", exc_info=True)
    error_message = e.response.get('Error', {}).get('Message', "Unknown AWS error")
    return build_response(500, f"AWS ClientError: {error_message}")
