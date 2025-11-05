from fastapi import HTTPException, Depends
from fastapi import APIRouter, Query
from typing import List, Optional
from configuration.mongoDbConfig import db
from models.studentModels import Student
from services.authentication import get_current_user
router = APIRouter()


@router.get("/get-all-students")
def get_all_students(current_user: dict = Depends(get_current_user)):
    res = list(db.students.find({}, {"_id": 0}))
    return res


@router.get("/get-student/{student_id}")
def get_student_by_id(student_id: int, current_user: dict = Depends(get_current_user)):
    student = db.students.find_one({"id": student_id}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/students", response_model=List[Student])
def get_students(
        current_user: dict = Depends(get_current_user),
        grade: Optional[str] = Query(None, description="Filter by grade"),
        name: Optional[str] = Query(None, description="Search by name"),
        roll_no: Optional[int] = Query(None, description="Search by roll number")
):
    query = {}

    # Filter by grade
    if grade:
        query["grade"] = grade

    # Search by name
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    # Search by roll number
    if roll_no:
        query["roll_no"] = roll_no

    students = list(db.students.find(query, {"_id": 0}))
    return students



