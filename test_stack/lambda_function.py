from aws_cdk import Duration
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_lambda_python_alpha as lambda_python
from constructs import Construct


class LambdaFunction(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        user_pool: cognito.IUserPool,
    ) -> None:
        super().__init__(scope, id)

        lambda_function = lambda_python.PythonFunction(
            self,
            "LambdaFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            entry="test_stack/functions/test_function",
            timeout=Duration.seconds(30),
            environment={
                "USER_POOL_ID": user_pool.user_pool_id,
            },
        )

        lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["cognito-idp:*"],
                resources=[user_pool.user_pool_arn],
            )
        )
