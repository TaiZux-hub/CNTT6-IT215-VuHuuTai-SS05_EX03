from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]

registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]


class RegistrationCreate(BaseModel):
    student_id: int
    course_id: int


@app.post("/registrations", status_code=status.HTTP_201_CREATED)
def create_registration(registration: RegistrationCreate):
    student_exists = False

    for student in students:
        if student["id"] == registration.student_id:
            student_exists = True
            break

    if student_exists is False:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    selected_course = None

    for course in courses:
        if course["id"] == registration.course_id:
            selected_course = course
            break

    if selected_course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    for existing_registration in registrations:
        if (
            existing_registration["student_id"] == registration.student_id
            and existing_registration["course_id"] == registration.course_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Student already registered this course"
            )

    current_count = 0

    for existing_registration in registrations:
        if existing_registration["course_id"] == registration.course_id:
            current_count += 1

    if current_count >= selected_course["capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Course is full"
        )

    new_registration = {
        "id": len(registrations) + 1,
        "student_id": registration.student_id,
        "course_id": registration.course_id
    }

    registrations.append(new_registration)

    return {
        "message": "Register successfully",
        "data": new_registration
    }