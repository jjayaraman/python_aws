from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_logs as logs,
    RemovalPolicy, Duration,
)

from aws_cdk.aws_dynamodb import Attribute
from constructs import Construct

# Lambda Constants
RUNTIME_PYTHON = _lambda.Runtime.PYTHON_3_10
MEMORY_SIZE = 128
TIMEOUT = Duration.seconds(5)
RETENTION_DAYS = logs.RetentionDays.ONE_WEEK


# Lambda
class DynamodbCrudStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB
        ddb = dynamodb.Table(self, "Users", table_name="Users",
                             partition_key=Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
                             read_capacity=2,
                             write_capacity=2, billing_mode=dynamodb.BillingMode.PROVISIONED,
                             removal_policy=RemovalPolicy.DESTROY)

        # Lambdas
        get_users_lambda = _lambda.Function(self, "get_users", handler="get_users.lambda_handler",
                                            code=_lambda.Code.from_asset("dynamodb_crud/lambda"),
                                            runtime=RUNTIME_PYTHON,
                                            memory_size=MEMORY_SIZE, timeout=TIMEOUT,
                                            log_retention=RETENTION_DAYS)

        create_user_lambda = _lambda.Function(self, "create_user", handler="create_user.lambda_handler",
                                              code=_lambda.Code.from_asset("dynamodb_crud/lambda"),
                                              runtime=RUNTIME_PYTHON,
                                              memory_size=MEMORY_SIZE, timeout=TIMEOUT,
                                              log_retention=RETENTION_DAYS)

        update_user_lambda = _lambda.Function(self, "update-user", handler="update_user.lambda_handler",
                                              code=_lambda.Code.from_asset("dynamodb_crud/lambda"),
                                              runtime=RUNTIME_PYTHON,
                                              memory_size=MEMORY_SIZE, timeout=TIMEOUT,
                                              log_retention=RETENTION_DAYS
                                              )

        # API Gateway
        user_api = apigateway.RestApi(self, 'user_service')

        users_resource = user_api.root.add_resource('users')
        users_resource.add_method('GET', apigateway.LambdaIntegration(get_users_lambda))

        user_resource = user_api.root.add_resource('user')
        user_resource.add_method('POST', apigateway.LambdaIntegration(create_user_lambda))

        user_resource_put = user_resource.add_resource("{id}")
        user_resource_put.add_method("PUT", apigateway.LambdaIntegration(update_user_lambda))

        # Permissions
        ddb.grant_read_data(get_users_lambda)
        ddb.grant_write_data(create_user_lambda)
        ddb.grant_write_data(update_user_lambda)

        # Destroy policy
        get_users_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        create_user_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        update_user_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        user_api.apply_removal_policy(RemovalPolicy.DESTROY)
