from aws_cdk import (
    Stack,
    aws_lambda as _lambda, Duration,
    aws_s3 as _s3, RemovalPolicy,
    aws_s3_notifications as s3_notifications,
    aws_logs as logs,
)
from constructs import Construct

# CDK constants
RUNTIME_PYTHON = _lambda.Runtime.PYTHON_3_10
MEMORY_SIZE = 2048
TIMEOUT = Duration.minutes(15)
RETENTION_DAYS = logs.RetentionDays.ONE_WEEK
SOURCE_S3_BUCKET_NAME = "jaysource"
TARGET_S3_BUCKET_NAME = "s3-unzip-python"


class UnzipStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        source_bucket = _s3.Bucket.from_bucket_name(self, id="SourceBucket", bucket_name=SOURCE_S3_BUCKET_NAME)

        unzip_s3 = _s3.Bucket(self, "s3-unzip-python", bucket_name=TARGET_S3_BUCKET_NAME,
                              removal_policy=RemovalPolicy.DESTROY, auto_delete_objects=True)

        # Lambda layer
        utils_layer = _lambda.LayerVersion(self, "utils_layer",
                                           code=_lambda.Code.from_asset("unzip/lambda/layer"),
                                           compatible_runtimes=[RUNTIME_PYTHON])

        unzip_lambda = _lambda.Function(self, "UnzipFunction",
                                        runtime=RUNTIME_PYTHON,
                                        code=_lambda.Code.from_asset("unzip/lambda"),
                                        handler="unzip_lambda.handler",
                                        memory_size=MEMORY_SIZE,
                                        timeout=TIMEOUT,
                                        log_retention=RETENTION_DAYS,
                                        layers=[utils_layer],
                                        environment={
                                            "destination_s3_bucket": unzip_s3.bucket_name
                                        })

        source_bucket.grant_read_write(unzip_lambda)
        unzip_s3.grant_write(unzip_lambda)

        notification = s3_notifications.LambdaDestination(unzip_lambda)
        source_bucket.add_event_notification(_s3.EventType.OBJECT_CREATED, notification,
                                             _s3.NotificationKeyFilter(suffix=".zip"))
