import boto3
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Connect to DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv("DYNAMODB_ENDPOINT"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("REGION_NAME"),
)

def create_table():
    table = dynamodb.create_table(
        TableName="Students",
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"}  # Partition key
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"}  # String type
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )
    table.wait_until_exists()
    print(f"Table {table.table_name} created successfully!")

if __name__ == "__main__":
    create_table()
