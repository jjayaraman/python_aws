from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb, RemovalPolicy
)
from aws_cdk.aws_dynamodb import Attribute
from constructs import Construct


class DynamodbCrudStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        dynamodb.Table(self, "Employee", table_name="Employee",
                       partition_key=Attribute(name="employee_id", type=dynamodb.AttributeType.STRING), read_capacity=2,
                       write_capacity=2, billing_mode=dynamodb.BillingMode.PROVISIONED,
                       removal_policy=RemovalPolicy.DESTROY)
