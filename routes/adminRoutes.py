from fastapi import APIRouter, HTTPException, Depends
from models.adminModels import Auth, Admin, _now_ts
from models.studentModels import Student
from configuration.mongoDbConfig import db
from passlib.context import CryptContext
from services.authentication import create_access_token, verify_admin
from datetime import datetime

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/admin-signup")
def admin_signup(res: Admin):
    existing_admin = db.admin.find_one({
        "$or": [
            {"username": res.username},
            {"email": res.email}
        ]
    })

    if existing_admin:
        if existing_admin.get("username") == res.username:
            raise HTTPException(status_code=400, detail="Username already exists")
        if existing_admin.get("email") == res.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = pwd_context.hash(res.password)
    admin_doc = {
        "username": res.username,
        "password": hashed_password,
        "email": res.email,
        "role": "admin",
        "created": datetime.now(),
        "updated": datetime.now(),
    }
    db.admin.insert_one(admin_doc)
    return {"message": "Admin registered successfully", "username": res.username}


@router.post("/admin-login")
def admin_login(res: Auth):
    admin = db.admin.find_one({"username": res.username})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    if not pwd_context.verify(res.password, admin.get("password", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Include role in token
    access_token = create_access_token(data={"sub": res.username, "role": "admin"})

    # sanitize admin object before returning
    admin_safe = {k: v for k, v in admin.items() if k not in ("password", "_id")}
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer", "admin": admin_safe}


@router.get("/admin-dashboard")
def admin_dashboard(current_admin: dict = Depends(verify_admin)):
    return {"message": f"Welcome, {current_admin['username']}! This is your admin dashboard."}


@router.post("/admin-add-student")
def add_student(student: Student, current_admin: dict = Depends(verify_admin)):
    db.students.insert_one(student.model_dump())
    return {"message": "Student added successfully", "student": student}


@router.delete("/admin-delete-student/{student_id}")
def delete_student(student_id: int, current_admin: dict = Depends(verify_admin)):
    result = db.students.delete_one({"id": student_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}


@router.put("/admin-update-student/{student_id}")
def update_student(student_id: int, student: Student, current_admin: dict = Depends(verify_admin)):
    # Check if student exists
    existing_student = db.students.find_one({"id": student_id})
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update student fields
    update_data = student.model_dump(exclude={"created"}, exclude_unset=True)  # Convert Pydantic model to dict
    update_data["updated_at"] = _now_ts()
    db.students.update_one({"id": student_id}, {"$set": update_data})

    # Fetch updated student to return
    updated_student = db.students.find_one({"id": student_id}, {"_id": 0})
    return {"message": "Student updated successfully", "student": updated_student}
