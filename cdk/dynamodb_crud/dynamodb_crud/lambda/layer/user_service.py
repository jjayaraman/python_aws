"""
Helper service to create CRUD operations on Users table in DynamoDB
"""

import logging
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# DynamoDB setup
USER_TABLE = "Users"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(USER_TABLE)


def create(user) -> dict:
    try:
        response = table.put_item(Item=user)
        return response
    except Exception as e:
        logger.error(f"Exception in create: {e}")
        raise e


def update(user_id: str, timestamp: str, first_name: str, last_name: str) -> dict:
    try:

        partition_key = {"user_id": user_id, "timestamp": timestamp}
        update_expression = "SET #first_name = :first_name, #last_name = :last_name"
        expression_attribute_names = {"#first_name": "first_name", "#last_name": "last_name"}
        expression_attribute_values = {":first_name": first_name, ":last_name": last_name}

        response = table.update_item(Key=partition_key, UpdateExpression=update_expression,
                                     ExpressionAttributeNames=expression_attribute_names,
                                     ExpressionAttributeValues=expression_attribute_values,
                                     ReturnValues="UPDATED_NEW")
        return response
    except Exception as e:
        logger.error(f"Exception in update : {e}")
        raise e


def delete(user_id: str, timestamp: str):
    logger.debug(f"user_id {user_id}, timestamp: {timestamp}")
    try:
        # check if user exists
        exists = check_if_user_exists(user_id, timestamp)
        print(f"user exists: {exists}")
        # Delete user
        if exists:
            key = {"user_id": user_id, "timestamp": timestamp}
            response = table.delete_item(Key=key)
            return response
        else:
            return None
    except Exception as e:
        logger.error(f"Exception in delete e : {str(e)}")
        raise e


def get_users():
    try:
        logger.debug("get_users called..")
        response = table.scan()
        return response
    except Exception as e:
        logger.error(f"Exception in get_users is e : {str(e)}")
        raise e


def get_user_by_id(user_id: str, timestamp: str):
    try:
        key = {"user_id": user_id, "timestamp": timestamp}
        response = table.get_item(Key=key)
        # response = table.query(KeyConditionExpression=Key('user_id').eq(user_id))
        logger.debug(f"response: {response}")
        # Return the item if it exists, else None
        return response.get('Item', None)
    except Exception as e:
        logger.error(f"Exception in get_user is e : {str(e)}")
        raise e


def search_users(first_name: Any, last_name: Any):
    global response
    try:
        if first_name and last_name:
            response_fn = table.query(IndexName='first_name_gsi',
                                      KeyConditionExpression=Key('first_name').eq(first_name))

            response_ln = table.query(IndexName='last_name_gsi',
                                      KeyConditionExpression=Key('last_name').eq(last_name))
            response = [item for item in response_fn if item in response_ln]

        elif first_name and not last_name:
            response = table.query(IndexName='first_name_gsi',
                                   KeyConditionExpression=Key('first_name').eq(first_name))

        elif not first_name and last_name:
            response = table.query(IndexName='last_name_gsi',
                                   KeyConditionExpression=Key('last_name').eq(last_name))

        return response

    except Exception as e:
        raise e


def check_if_user_exists(user_id: str, timestamp: str):
    user = get_user_by_id(user_id, timestamp)
    logger.info(f"user : {user}")
    if user is not None:
        return True
    return False
