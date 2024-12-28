from aws_cdk import Stack, aws_s3
from constructs import Construct


class HelloStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        aws_s3.Bucket(self, 'bucket1', bucket_name='jaycdkbucket321')

        # example resource
        # queue = sqs.Queue(
        #     self, "HelloQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # Define the Lambda function
        # hello_lambda = _lambda.Function(
        #     self,
        #     "HelloLambdaHandler",
        #     runtime=_lambda.Runtime.PYTHON_3_9,  # Specify the Python runtime
        #     handler="hello.handler",  # File is hello.py, function is handler
        #     code=_lambda.Code.from_asset("lambda"),  # Path to Lambda code
        # )`
