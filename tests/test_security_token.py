import uuid

import requests
import json


def test_cognito_credentials(session):
    # Use boto3 session patched to point to localstack
    cognito_client = session.client("cognito-idp")
    lambda_client = session.client("lambda")

    # Get user pool id

    lambda_response = cognito_client.list_user_pools(MaxResults=1)
    user_pool_id = lambda_response["UserPools"][0]["Id"]
    print(f"user_pool_id: {user_pool_id}")

    # get client id
    lambda_response = cognito_client.list_user_pool_clients(UserPoolId=user_pool_id)
    user_pool_client_id = lambda_response["UserPoolClients"][0]["ClientId"]
    print(f"user_pool_client_id: {user_pool_client_id}")

    # get lambda_function
    lambda_response = lambda_client.list_functions()
    lambda_function_arn = lambda_response["Functions"][0]["FunctionArn"]

    # Add a user
    email = f"{uuid.uuid4().hex[:6]}@example.org"
    pw = "8c01d1A%"
    cognito_client.sign_up(
        ClientId=user_pool_client_id,
        Username=email,
        Password=pw,
        UserAttributes=[
            {"Name": "email", "Value": email},
        ],
    )
    cognito_client.admin_confirm_sign_up(UserPoolId=user_pool_id, Username=email)

    # invoke lambda function
    lambda_response = lambda_client.invoke(
        FunctionName=lambda_function_arn,
        Payload=json.dumps({"foo": "bar"}).encode(),
    )

    lambda_payload = lambda_response["Payload"].read().decode()
    print(f"lambda_payload: {lambda_payload}")
    assert len(json.loads(lambda_payload)["usernames"]) > 0
