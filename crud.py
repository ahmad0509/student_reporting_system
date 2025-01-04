import boto3
import os

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv("DYNAMODB_ENDPOINT"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("REGION_NAME"),
)

students_table = dynamodb.Table("Students")
print(f"Students table status: {students_table.table_status}")

def add_student(data):
    
        students_table.put_item(Item=data)
    

def get_students():
    response = students_table.scan()
    return response["Items"]

def get_student_by_id(student_id):
    response = students_table.get_item(Key={"id": student_id})
    return response.get("Item")

def get_average_score():
    try:
        # Fetch all students
        students = get_students()
        
        # Check if there are any students
        if not students:
            return {"message": "No students found to calculate the average."}
        
        # Extract scores and calculate the average
        scores = [float(student["score"]) for student in students]
        average_score = sum(scores) / len(scores)
        
        # Return the result
        return {
            "message": "Average score calculated successfully.",
            "average_score": round(average_score, 2)
        }
    except Exception as e:
        print(f"Error calculating average score: {e}")
        return {"error": "Failed to calculate average score"}    