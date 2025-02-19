from fastapi import FastAPI
from pydantic import BaseModel
from decimal import Decimal
from fastapi.responses import FileResponse
from visualize import generate_score_chart
from crud import add_student, get_students, get_student_by_id, get_average_score, get_students_by_city, get_students_by_gender, get_chapter_scores

app = FastAPI()


class Student(BaseModel):
    id: str
    name: str
    grade: str
    city: str
    gender: str
    math_total: Decimal
    science_total: Decimal
    chapter_marks: dict

class AverageScoresResponse(BaseModel):
    average_math_score: float
    average_science_score: float
    total_students: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Reporting System!"}

@app.get("/students")
def list_students():
    return get_students()

@app.get("/students/{student_id}")
def get_student(student_id: str):
    return get_student_by_id(student_id)

@app.get("/average", response_model=AverageScoresResponse)
async def get_average():
    
    data = {'average_math_score': 73.9, 'average_science_score': 71.7, 'total_students': 20}
    return get_average_score()

@app.get("/students/city/{city}")
def students_by_city(city: str):
    return get_students_by_city(city)

@app.get("/students/gender/{gender}")
def students_by_gender(gender: str):
    return get_students_by_gender(gender)

@app.get("/students/{student_id}/chapters")
def student_chapter_scores(student_id: str):
    return get_chapter_scores(student_id)

@app.get("/generate-chart", response_class=FileResponse)
def get_score_chart():
    chart_path = generate_score_chart()
    
    if chart_path:
        return FileResponse(chart_path, media_type="image/png", filename="score_chart.png")
    return {"error": "Chart generation failed"}