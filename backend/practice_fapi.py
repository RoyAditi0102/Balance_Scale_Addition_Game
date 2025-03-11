from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name":"John",
        "age" : 17,
        "year": "year 12"
    },
    2: {
        "name":"Sam",
        "age": 12,
        "year": "year 6"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year:str

@app.get("/")
def index():
    return {"go to get-student"}

#getting by student id
@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(...,description="Enter the value of student ID desired", gt = 0, lt = 5)):
    return students[student_id]

#getting by name (optional)
@app.get("/get-by-name")
def get_student(*, name : Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return "Data Not Found"

#getting by name and id (Combining path and query parameters)
@app.get("/get-by-id-or-name")
def get_student(*, student_id: Optional[int], name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return "Data no found"

@app.post("/create-student/{student_id}")
def create_student(student_id : int, student : Student):
    if student_id in students:
        return {"Error":"Student exists"}
    students[student_id] = student
    return students[student_id]