from typing import Any

from aws_cdk import Stack
from constructs import Construct

from test_stack.auth import CognitoClient
from test_stack.lambda_function import LambdaFunction


class TestStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO: read in environment dev/prod
        cognito_client = CognitoClient(
            self, "TestCognitoClient", cognito_domain_prefix="test-dev"
        )
        LambdaFunction(self, "LambdaFunction", user_pool=cognito_client.user_pool)
