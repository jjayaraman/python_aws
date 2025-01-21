from aws_cdk import (
    Stack,
    aws_lambda as _lambda, Duration,
    aws_s3 as _s3, RemovalPolicy,
    aws_s3_notifications as s3_notifications
)
from aws_cdk.aws_lambda_event_sources import S3EventSource
from constructs import Construct


class UnzipStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        unzip_s3 = _s3.Bucket(self, "s3-unzip-python", bucket_name="s3-unzip-python", removal_policy=RemovalPolicy.DESTROY, auto_delete_objects=True)

        unzip_lambda = _lambda.Function(self, "UnzipFunction",
                                        runtime=_lambda.Runtime.PYTHON_3_10,
                                        code=_lambda.Code.from_asset("unzip/lambda"),
                                        handler="unzip_lambda.handler",
                                        timeout=Duration.seconds(30)
                                        )

        unzip_s3.grant_read_write(unzip_lambda)

        notification = s3_notifications.LambdaDestination(unzip_lambda)
        unzip_s3.add_event_notification(_s3.EventType.OBJECT_CREATED, notification, _s3.NotificationKeyFilter(suffix=".zip"))

