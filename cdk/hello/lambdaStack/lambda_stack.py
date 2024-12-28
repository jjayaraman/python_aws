from aws_cdk import (Stack, Duration,
                     aws_lambda as _lambda,
                     aws_apigateway as apigateway)

from constructs import Construct


class LambdaStack(Stack):

    def __init__(self, scope: Construct, constructor_id: str, **kwargs) -> None:
        super().__init__(scope, constructor_id, **kwargs)

        # Add aws resources
        my_lambda = _lambda.Function(self, 'MyLambda', code=_lambda.Code.from_asset('lambdaStack/src'),
                                     handler='my_lambda.lambda_handler',
                                     runtime=_lambda.Runtime.PYTHON_3_10,
                                     memory_size=128,
                                     timeout=Duration.seconds(5),
                                     )

        my_apigw = apigateway.LambdaRestApi(self, "MyApiGw", handler=my_lambda, proxy=True)

        my_resource = my_apigw.root.add_resource("hello")
        my_resource.add_method("GET")
