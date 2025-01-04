from dotenv import load_dotenv
import os

load_dotenv()
from fastapi import FastAPI
from crud import add_student, get_students, get_student_by_id, get_average_score
import uuid
from visualize import generate_score_chart


app = FastAPI()
from pydantic import BaseModel
from decimal import Decimal

class Student(BaseModel):
    name: str
    grade: str
    subject: str
    score: Decimal 

@app.post("/students")
def create_student(student: Student):
    try:
        student_id = str(uuid.uuid4())
        data = student.dict()
        data["id"] = student_id
        
        data["score"] = Decimal(str(data["score"]))
        add_student(data)
        return {"message": "Student added successfully", "id": student_id}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Failed to add student"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Reporting System!"}



@app.get("/students")
def list_students():
    return get_students()

@app.get("/students/{student_id}")
def get_student(student_id: str):
    return get_student_by_id(student_id)

@app.get("/students/chart")
def student_chart():
    generate_score_chart()
    return {"message": "Chart generated and saved as score_chart.png"}

@app.get("/students/average_score")
def average_score():
    return get_average_score()
