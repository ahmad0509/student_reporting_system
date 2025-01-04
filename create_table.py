import boto3
import os

# Load environment variables
endpoint_url = os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8000")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", "local")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", "local")
region_name = os.getenv("REGION_NAME", "us-west-2")

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=endpoint_url,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name,
)

# Create table
try:
    table_name = "Students"
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"},  # Partition key
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},  # String type
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        },
    )
    table.wait_until_exists()
    print(f"Table {table_name} created successfully!")
except Exception as e:
    print(f"Error: {e}")
