from fastapi import HTTPException, Depends
from fastapi import APIRouter, Query
from typing import List, Optional
from configuration.mongoDbConfig import db
from models.studentModels import Student
from services.authentication import get_current_user
from pymongo import ASCENDING, DESCENDING
import re


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


@router.get("/students")
def get_students(
        current_user: dict = Depends(get_current_user),
        grade: Optional[str] = Query(None, description="Filter by grade"),
        name: Optional[str] = Query(None, description="Search by name"),
        roll_no: Optional[int] = Query(None, description="Search by roll number"),
        sort_by: Optional[str] = Query("id", description="Sort by field (e.g., id, name, roll_no, age, grade)"),
        sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Records per page")
):
    query = {}

    # Apply filters
    if grade:
        query["grade"] = grade
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if roll_no:
        query["roll_no"] = roll_no

    # sort direction
    sort_direction = ASCENDING if sort_order.lower() == "asc" else DESCENDING

    # Pagination calculations
    skip = (page - 1) * limit

    # Total count before pagination
    total_count = db.students.count_documents(query)

    # Fetch paginated & sorted results
    students = list(
        db.students.find(query, {"_id": 0})
        .sort(sort_by, sort_direction)
        .skip(skip)
        .limit(limit)
    )

    return {
        "total_records": total_count,
        "page": page,
        "limit": limit,
        "students": students
    }
