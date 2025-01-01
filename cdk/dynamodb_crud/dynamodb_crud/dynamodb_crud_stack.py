from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_logs as logs,
    RemovalPolicy, Duration,
)

from aws_cdk.aws_dynamodb import Attribute, AttributeType
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
                             sort_key=Attribute(name="timestamp", type=AttributeType.STRING),
                             read_capacity=2,
                             write_capacity=2, billing_mode=dynamodb.BillingMode.PROVISIONED,
                             removal_policy=RemovalPolicy.DESTROY)
        ddb.add_global_secondary_index(index_name="first_name_gsi",
                                       partition_key=Attribute(name="first_name", type=AttributeType.STRING))
        ddb.add_global_secondary_index(index_name="last_name_gsi",
                                       partition_key=Attribute(name="last_name", type=AttributeType.STRING))

        # API Gateway

        # Lambda layer
        user_service_layer = _lambda.LayerVersion(self, "user_service_layer",
                                                  code=_lambda.Code.from_asset("dynamodb_crud/lambda/layer"),
                                                  compatible_runtimes=[RUNTIME_PYTHON])

        # Lambdas
        get_users_lambda = _lambda.Function(self, "get_users", handler="get_users.lambda_handler",
                                            code=_lambda.Code.from_asset("dynamodb_crud/lambda"),
                                            runtime=RUNTIME_PYTHON,
                                            memory_size=MEMORY_SIZE, timeout=TIMEOUT,
                                            log_retention=RETENTION_DAYS,
                                            layers=[user_service_layer]
                                            )
        search_users_lambda = _lambda.Function(self, "search_users", handler="search_users.lambda_handler",
                                               code=_lambda.Code.from_asset("dynamodb_crud/lambda"),
                                               runtime=RUNTIME_PYTHON,
                                               memory_size=MEMORY_SIZE, timeout=TIMEOUT,
                                               log_retention=RETENTION_DAYS,
                                               layers=[user_service_layer])

        create_user_lambda = _lambda.Function(self, "create_user", handler="create_user.lambda_handler",
                                              code=_lambda.Code.from_asset("dynamodb_crud/lambda"),
                                              runtime=RUNTIME_PYTHON,
                                              memory_size=MEMORY_SIZE, timeout=TIMEOUT,
                                              log_retention=RETENTION_DAYS,
                                              layers=[user_service_layer]
                                              )

        update_user_lambda = _lambda.Function(self, "update-user", handler="update_user.lambda_handler",
                                              code=_lambda.Code.from_asset("dynamodb_crud/lambda"),
                                              runtime=RUNTIME_PYTHON,
                                              memory_size=MEMORY_SIZE, timeout=TIMEOUT,
                                              log_retention=RETENTION_DAYS,
                                              layers=[user_service_layer]
                                              )

        delete_user_lambda = _lambda.Function(self, "delete_user", handler="delete_user.lambda_handler",
                                              code=_lambda.Code.from_asset("dynamodb_crud/lambda"),
                                              runtime=RUNTIME_PYTHON,
                                              memory_size=MEMORY_SIZE, timeout=TIMEOUT,
                                              log_retention=RETENTION_DAYS,
                                              layers=[user_service_layer]
                                              )

        # APIs
        user_api = apigateway.RestApi(self, 'user_service')

        users_resource = user_api.root.add_resource('users')
        users_resource.add_method('GET', apigateway.LambdaIntegration(get_users_lambda))

        search_resource = users_resource.add_resource("search")
        search_resource.add_method("GET", apigateway.LambdaIntegration(search_users_lambda))

        user_resource = user_api.root.add_resource('user')
        user_resource.add_method('POST', apigateway.LambdaIntegration(create_user_lambda))

        user_resource_id = user_resource.add_resource("{id}").add_resource("{timestamp}")
        user_resource_id.add_method("PUT", apigateway.LambdaIntegration(update_user_lambda))
        user_resource_id.add_method("DELETE", apigateway.LambdaIntegration(delete_user_lambda))

        # Permissions
        ddb.grant_read_data(get_users_lambda)
        ddb.grant_read_data(search_users_lambda)
        ddb.grant_write_data(create_user_lambda)
        ddb.grant_write_data(update_user_lambda)
        ddb.grant_full_access(delete_user_lambda)

        # Destroy policy
        get_users_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        search_users_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        create_user_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        update_user_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        delete_user_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        user_api.apply_removal_policy(RemovalPolicy.DESTROY)
