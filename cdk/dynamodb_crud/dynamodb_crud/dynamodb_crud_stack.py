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
        create_user_lambda = _lambda.Function(self, "create_user", handler="create_user.lambda_handler",
                                              code=_lambda.Code.from_asset("dynamodb_crud/lambda"),
                                              runtime=_lambda.Runtime.PYTHON_3_10,
                                              memory_size=128, timeout=Duration.seconds(5),
                                              log_retention=logs.RetentionDays.ONE_WEEK)

        get_users_lambda = _lambda.Function(self, "get_users", handler="get_users.lambda_handler",
                                            code=_lambda.Code.from_asset("dynamodb_crud/lambda"),
                                            runtime=_lambda.Runtime.PYTHON_3_10,
                                            memory_size=128, timeout=Duration.seconds(5),
                                            log_retention=logs.RetentionDays.ONE_WEEK)

        # API Gateways
        create_user_api = apigateway.LambdaRestApi(self, 'create_user_api', handler=create_user_lambda)
        create_user_resource = create_user_api.root.add_resource('user')
        create_user_resource.add_method('POST')

        get_users_api = apigateway.LambdaRestApi(self, 'get_users_api', handler=get_users_lambda)
        get_users_resource = get_users_api.root.add_resource('users')
        get_users_resource.add_method('GET')

        # Permissions
        ddb.grant_write_data(create_user_lambda)
        ddb.grant_read_data(get_users_lambda)

        # Destroy policy
        create_user_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        get_users_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        create_user_api.apply_removal_policy(RemovalPolicy.DESTROY)
        get_users_api.apply_removal_policy(RemovalPolicy.DESTROY)
