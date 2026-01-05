from fastapi import FastAPI, status
from pydantic import BaseModel
from .producer import kafka_producer

app = FastAPI()

class Student(BaseModel):
    id: int
    score: str


@app.get("/")
def home():
    return {"message":"Hello, World"}

@app.post("/marks", status_code=status.HTTP_201_CREATED)
async def add_student(student: Student):
    student_data = student.model_dump()
    kafka_producer.publish(topic="marks", data=student_data)
    return {"status": "sent", "data": student_data}
