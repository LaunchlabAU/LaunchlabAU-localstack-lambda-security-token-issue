import json
import os

import boto3

USER_POOL_ID = os.environ["USER_POOL_ID"]


def handler(event, context):
    client = boto3.client("cognito-idp", verify=False)
    response = client.list_users(UserPoolId=USER_POOL_ID)
    return {"usernames": [u["Username"] for u in response["Users"]]}
