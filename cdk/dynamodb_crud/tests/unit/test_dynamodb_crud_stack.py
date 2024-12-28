import aws_cdk as core
import aws_cdk.assertions as assertions

from dynamodb_crud.dynamodb_crud_stack import DynamodbCrudStack

# example tests. To run these tests, uncomment this file along with the example
# resource in dynamodb_crud/dynamodb_crud_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DynamodbCrudStack(app, "dynamodb-crud")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
