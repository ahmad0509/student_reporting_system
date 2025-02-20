import boto3
import csv
import os
from decimal import Decimal
 
# Initialize DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=os.getenv("DYNAMODB_ENDPOINT"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("REGION_NAME"),
)

table_name = "Students"

def create_students_table():
    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
    if table_name in existing_tables:
        print(f"Table '{table_name}' already exists.")
        return
    
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    table.wait_until_exists()
    print(f"Table '{table_name}' created successfully!")

def load_data(csv_file):
    table = dynamodb.Table(table_name)
    
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            student_id = str(row["Student_ID"])

            # Initialize student data
            student_data = {
                "id": student_id,
                "name": row["Name"],
                "grade": row["Grade"],
                "city": row["City"],
                "gender": row["Gender"],
                "math_total": Decimal(row["Math_Total"]),
                "science_total": Decimal(row["Science_Total"]),
                "math_chapters": {},  # Store Math chapters separately
                "science_chapters": {},  # Store Science chapters separately
            }

            # Separate Math and Science chapter marks
            for key, value in row.items():
             if key.startswith("Ch") and "_Math_" in key:  # Example: Ch1_Math_Real Numbers
                 try:
                        student_data["math_chapters"][key] = Decimal(value)
                 except:
                        student_data["math_chapters"][key] = Decimal(0)  # Default to 0 if invalid
             elif key.startswith("Ch") and "_Science_" in key:  # Example: Ch1_Science_Chemical Reactions
                try:
                        student_data["science_chapters"][key] = Decimal(value)
                except:
                 student_data["science_chapters"][key] = Decimal(0)




    print("Student data loaded successfully!")

if __name__ == "__main__":
    create_students_table()  
    csv_filename = "/app/student_data.csv"  
    load_data(csv_filename)
