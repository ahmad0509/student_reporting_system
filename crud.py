import boto3
import os
from decimal import Decimal

# Connect to DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=os.getenv("DYNAMODB_ENDPOINT"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("REGION_NAME"),
)

students_table = dynamodb.Table("Students")

def add_student(data):
    students_table.put_item(Item=data)

def get_students():
    response = students_table.scan()
    return response["Items"]

def get_student_by_id(student_id):
    response = students_table.get_item(Key={"id": student_id})
    return response.get("Item")

def get_average_score():
    students = get_students()
    
    if not students:
        return {"message": "No students found."}

    total_math = sum(float(s["math_total"]) if "math_total" in s else 0 for s in students)
    total_science = sum(float(s["science_total"]) if "science_total" in s else 0 for s in students)
    count = len(students)
    
    avg_math = round(total_math / count, 2) if count else 0
    avg_science = round(total_science / count, 2) if count else 0

    return {
        "average_math_score": avg_math,
        "average_science_score": avg_science,
        "total_students": count,
    }


def get_students_by_city(city):
    response = students_table.scan(
        FilterExpression="city = :city", ExpressionAttributeValues={":city": city}
    )
    return response.get("Items", [])

def get_students_by_gender(gender):
    response = students_table.scan(
        FilterExpression="gender = :gender", ExpressionAttributeValues={":gender": gender}
    )
    return response.get("Items", [])

def get_chapter_scores(student_id):
    student = get_student_by_id(student_id)
    if not student:
        return {"message": "Student not found"}
    
    return {
        "math_chapters": student.get("math_chapters", {}),
        "science_chapters": student.get("science_chapters", {})
    }
