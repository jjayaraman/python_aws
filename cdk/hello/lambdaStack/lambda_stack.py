from aws_cdk import (Stack, Duration)
from aws_cdk.aws_lambda import Function, Runtime, Code

from constructs import Construct


class LambdaStack(Stack):

    def __init__(self, scope: Construct, constructor_id: str, **kwargs) -> None:
        super().__init__(scope, constructor_id, **kwargs)

        # Add aws resources
        Function(self, 'MyLambda', code=Code.from_asset('lambdaStack/src'), handler='my_lambda.lambda_handler',
                 runtime=Runtime.PYTHON_3_10,
                 memory_size=128,
                 timeout=Duration.seconds(5),
                 )
