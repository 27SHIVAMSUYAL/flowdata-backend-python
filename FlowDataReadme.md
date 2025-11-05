# FlowData - Student Management System

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Environment Configuration](#environment-configuration)
- [API Documentation](#api-documentation)
- [Authentication & Authorization](#authentication--authorization)
- [Security Features](#security-features)
- [Testing Guide](#testing-guide)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**FlowData** is a comprehensive student management system built with FastAPI and MongoDB. It implements role-based access control (RBAC) using JWT authentication, allowing different levels of access for administrators and regular users.

### Key Capabilities
- **Admin Users**: Full CRUD operations on student records
- **Regular Users**: Read-only access to student information
- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **MongoDB Integration**: Persistent storage with MongoDB Atlas
- **RESTful API**: Clean and well-documented API endpoints

---

## ✨ Features

### 🔐 Authentication & Authorization
- JWT-based authentication with role claims
- Password hashing using bcrypt
- Token expiration (configurable)
- Role-based access control (Admin/User)
- Protected routes with middleware

### 👥 User Management
- Admin signup and login
- Regular user signup and login
- Separate authentication flows
- Password security with hashing

### 📚 Student Management
- **Create**: Add new students (Admin only)
- **Read**: View all students or search by ID/filters (All authenticated users)
- **Update**: Modify student records (Admin only)
- **Delete**: Remove student records (Admin only)
- **Search & Filter**: Find students by name, grade, or roll number

### 🎨 Additional Features
- CORS support for frontend integration
- Pydantic models for data validation
- Automatic timestamp tracking (created_at, updated_at)
- Clean error handling with proper HTTP status codes

---

## 🛠️ Tech Stack

### Backend Framework
- **FastAPI** (v0.121.0) - Modern, fast web framework for building APIs
- **Uvicorn** (v0.38.0) - ASGI server

### Database
- **MongoDB** (via pymongo v4.15.3) - NoSQL database
- **MongoDB Atlas** - Cloud database hosting

### Authentication & Security
- **python-jose** (v3.3.0) - JWT token generation and verification
- **passlib** (v1.7.4) - Password hashing
- **bcrypt** (v4.0.1) - Secure password hashing algorithm

### Data Validation
- **Pydantic** (v2.12.3) - Data validation and settings management

### Additional Libraries
- **python-dotenv** (v1.2.1) - Environment variable management
- **python-multipart** (v0.0.20) - Form data parsing

---

## 📁 Project Structure

```
FlowDataProject/
│
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (not in git)
├── .gitignore                      # Git ignore file
├── FlowDataReadme.md               # This file
│
├── configuration/
│   └── mongoDbConfig.py            # MongoDB connection setup
│
├── models/
│   ├── adminModels.py              # Admin & Auth Pydantic models
│   ├── userModels.py               # User & UserAuth Pydantic models
│   └── studentModels.py            # Student Pydantic model
│
├── routes/
│   ├── adminRoutes.py              # Admin endpoints (protected)
│   ├── userRoutes.py               # User authentication endpoints
│   └── studentRoutes.py            # Student viewing endpoints
│
└── services/
    └── authentication.py           # JWT & authentication logic
```

### File Descriptions

#### Core Files
- **main.py**: FastAPI application initialization, router inclusion, CORS middleware
- **requirements.txt**: All Python package dependencies

#### Configuration
- **mongoDbConfig.py**: MongoDB client setup, database connection, ping test

#### Models (Pydantic)
- **adminModels.py**: `Admin` (signup), `Auth` (login) models
- **userModels.py**: `User` (signup), `UserAuth` (login) models
- **studentModels.py**: `Student` model with auto-generated timestamps

#### Routes
- **adminRoutes.py**: Admin signup/login, student CRUD operations (admin-only)
- **userRoutes.py**: User signup/login
- **studentRoutes.py**: Student viewing, searching, filtering (authenticated users)

#### Services
- **authentication.py**: JWT token creation, verification, role-based access control

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12+ installed
- MongoDB Atlas account (or local MongoDB instance)
- Git (optional, for cloning)

### Step 1: Clone or Download Project
```bash
git clone <your-repo-url>
cd FlowDataProject
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```env
MONGO_URI=
DB_NAME=students_db
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Important**: 
- Replace `<username>` and `<password>` with your MongoDB credentials
- Use a strong, random `SECRET_KEY` (generate with `openssl rand -hex 32`)
- Never commit `.env` to version control

### Step 5: Run the Application
```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

### Step 6: Access API Documentation
FastAPI provides interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## ⚙️ Environment Configuration
eg :

MONGO_URI=
DB_NAME=students_db
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `DB_NAME` | Database name | `students_db` |
| `SECRET_KEY` | JWT signing key (keep secret!) | `09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `60` |

### Generating a Secure Secret Key
```bash
# Using OpenSSL
openssl rand -hex 32

# Using Python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📖 API Documentation

### Base URL
```
http://localhost:8000
```

---

## 🔑 Authentication Endpoints

### 1. Admin Signup
**Endpoint**: `POST /admin-signup`

**Description**: Register a new admin user

**Request Body**:
```json
{
  "username": "admin1",
  "password": "securepass123",
  "email": "admin@example.com",
  "role": "admin"
}
```

**Response** (200 OK):
```json
{
  "message": "Admin registered successfully",
  "username": "admin1"
}
```

**Errors**:
- `400 Bad Request`: Admin already exists

---

### 2. Admin Login
**Endpoint**: `POST /admin-login`

**Description**: Login as admin and receive JWT token

**Request Body**:
```json
{
  "username": "admin1",
  "password": "securepass123"
}
```

**Response** (200 OK):
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "admin": {
    "username": "admin1",
    "email": "admin@example.com",
    "role": "admin",
    "created": 1699200000,
    "updated": 1699200000
  }
}
```

**Errors**:
- `404 Not Found`: Admin not found
- `401 Unauthorized`: Invalid credentials

---

### 3. User Signup
**Endpoint**: `POST /user-signup`

**Description**: Register a new regular user

**Request Body**:
```json
{
  "username": "user1",
  "password": "userpass123",
  "email": "user@example.com",
  "role": "user"
}
```

**Response** (200 OK):
```json
{
  "message": "User registered successfully",
  "username": "user1"
}
```

**Errors**:
- `400 Bad Request`: User already exists

---

### 4. User Login
**Endpoint**: `POST /user-login`

**Description**: Login as regular user and receive JWT token

**Request Body**:
```json
{
  "username": "user1",
  "password": "userpass123"
}
```

**Response** (200 OK):
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "username": "user1",
    "email": "user@example.com",
    "role": "user",
    "created": 1699200000,
    "updated": 1699200000
  }
}
```

**Errors**:
- `404 Not Found`: User not found
- `401 Unauthorized`: Invalid credentials

---

## 👨‍💼 Admin-Only Endpoints (Require Admin Role)

### 5. Admin Dashboard
**Endpoint**: `GET /admin-dashboard`

**Description**: Access admin dashboard

**Headers**:
```
Authorization: Bearer <ADMIN_TOKEN>
```

**Response** (200 OK):
```json
{
  "message": "Welcome, admin1! This is your admin dashboard."
}
```

**Errors**:
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User role insufficient (not admin)

---

### 6. Add Student (Admin Only)
**Endpoint**: `POST /admin-add-student`

**Description**: Create a new student record

**Headers**:
```
Authorization: Bearer <ADMIN_TOKEN>
```

**Request Body**:
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 16,
  "roll_no": 101,
  "grade": "10"
}
```

**Response** (200 OK):
```json
{
  "message": "Student added successfully",
  "student": {
    "id": 1,
    "name": "John Doe",
    "age": 16,
    "roll_no": 101,
    "grade": "10",
    "created_at": 1699200000,
    "updated_at": 1699200000
  }
}
```

**Errors**:
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User role insufficient

---

### 7. Update Student (Admin Only)
**Endpoint**: `PUT /admin-update-student/{student_id}`

**Description**: Update an existing student record

**Headers**:
```
Authorization: Bearer <ADMIN_TOKEN>
```

**Path Parameters**:
- `student_id` (integer): Student ID to update

**Request Body**:
```json
{
  "id": 1,
  "name": "John Updated",
  "age": 17,
  "roll_no": 101,
  "grade": "11"
}
```

**Response** (200 OK):
```json
{
  "message": "Student updated successfully",
  "student": {
    "id": 1,
    "name": "John Updated",
    "age": 17,
    "roll_no": 101,
    "grade": "11",
    "created_at": 1699200000,
    "updated_at": 1699210000
  }
}
```

**Errors**:
- `404 Not Found`: Student not found
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User role insufficient

---

### 8. Delete Student (Admin Only)
**Endpoint**: `DELETE /admin-delete-student/{student_id}`

**Description**: Delete a student record

**Headers**:
```
Authorization: Bearer <ADMIN_TOKEN>
```

**Path Parameters**:
- `student_id` (integer): Student ID to delete

**Response** (200 OK):
```json
{
  "message": "Student deleted successfully"
}
```

**Errors**:
- `404 Not Found`: Student not found
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User role insufficient

---

## 📚 Student Viewing Endpoints (All Authenticated Users)

### 9. Get All Students
**Endpoint**: `GET /get-all-students`

**Description**: Retrieve all student records

**Headers**:
```
Authorization: Bearer <USER_OR_ADMIN_TOKEN>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "age": 16,
    "roll_no": 101,
    "grade": "10",
    "created_at": 1699200000,
    "updated_at": 1699200000
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "age": 15,
    "roll_no": 102,
    "grade": "9",
    "created_at": 1699200100,
    "updated_at": 1699200100
  }
]
```

**Errors**:
- `401 Unauthorized`: Invalid or missing token

---

### 10. Get Student by ID
**Endpoint**: `GET /get-student/{student_id}`

**Description**: Retrieve a specific student by ID

**Headers**:
```
Authorization: Bearer <USER_OR_ADMIN_TOKEN>
```

**Path Parameters**:
- `student_id` (integer): Student ID

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 16,
  "roll_no": 101,
  "grade": "10",
  "created_at": 1699200000,
  "updated_at": 1699200000
}
```

**Errors**:
- `404 Not Found`: Student not found
- `401 Unauthorized`: Invalid or missing token

---

### 11. Search & Filter Students
**Endpoint**: `GET /students`

**Description**: Search students with optional filters

**Headers**:
```
Authorization: Bearer <USER_OR_ADMIN_TOKEN>
```

**Query Parameters** (all optional):
- `grade` (string): Filter by grade (e.g., "10")
- `name` (string): Search by name (case-insensitive, partial match)
- `roll_no` (integer): Search by exact roll number

**Examples**:
```bash
# Get all grade 10 students
GET /students?grade=10

# Search students with "john" in name
GET /students?name=john

# Get student by roll number
GET /students?roll_no=101

# Combine filters
GET /students?grade=10&name=john
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "age": 16,
    "roll_no": 101,
    "grade": "10",
    "created_at": 1699200000,
    "updated_at": 1699200000
  }
]
```

**Errors**:
- `401 Unauthorized`: Invalid or missing token

---

## 🔐 Authentication & Authorization

### JWT Token Structure
```json
{
  "sub": "username",
  "role": "admin" or "user",
  "exp": 1699286400
}
```

### Role-Based Access Control Matrix

| Route | Admin Token | User Token | No Token |
|-------|-------------|------------|----------|
| `POST /admin-signup` | ✅ Public | ✅ Public | ✅ Public |
| `POST /admin-login` | ✅ Public | ✅ Public | ✅ Public |
| `POST /user-signup` | ✅ Public | ✅ Public | ✅ Public |
| `POST /user-login` | ✅ Public | ✅ Public | ✅ Public |
| `GET /admin-dashboard` | ✅ Allow | ❌ 403 | ❌ 401 |
| `POST /admin-add-student` | ✅ Allow | ❌ 403 | ❌ 401 |
| `PUT /admin-update-student/{id}` | ✅ Allow | ❌ 403 | ❌ 401 |
| `DELETE /admin-delete-student/{id}` | ✅ Allow | ❌ 403 | ❌ 401 |
| `GET /get-all-students` | ✅ Allow | ✅ Allow | ❌ 401 |
| `GET /get-student/{id}` | ✅ Allow | ✅ Allow | ❌ 401 |
| `GET /students` | ✅ Allow | ✅ Allow | ❌ 401 |

### Using Tokens in Requests

**cURL Example**:
```bash
curl -X GET http://localhost:8000/get-all-students \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Postman**:
1. Go to Authorization tab
2. Select Type: "Bearer Token"
3. Paste your token in the Token field

**JavaScript Fetch**:
```javascript
fetch('http://localhost:8000/get-all-students', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
```

---

## 🛡️ Security Features

### 1. Password Security
- **Bcrypt Hashing**: All passwords hashed with bcrypt (cost factor 12)
- **No Plain Text**: Passwords never stored or transmitted in plain text
- **Salted Hashes**: Each password gets a unique salt

### 2. JWT Security
- **Signed Tokens**: All tokens signed with SECRET_KEY
- **Expiration**: Tokens expire after configured time (default 60 minutes)
- **Role Claims**: Role embedded in token payload for RBAC
- **Algorithm**: Uses HS256 (HMAC with SHA-256)

### 3. Authorization
- **Middleware Protection**: All sensitive routes protected with dependencies
- **Role Verification**: Admin routes verify `role == "admin"`
- **Token Validation**: Tokens validated on every protected request

### 4. Data Sanitization
- **No Password Exposure**: Passwords excluded from API responses
- **No Internal IDs**: MongoDB `_id` excluded from responses
- **Pydantic Validation**: All input validated with Pydantic models

### 5. CORS Configuration
- **Configurable Origins**: Currently allows all origins (adjust for production)
- **Credential Support**: Allows cookies/auth headers
- **Method Whitelist**: Supports all HTTP methods

### 6. Database Security
- **Connection String**: Stored in environment variable
- **Network Security**: MongoDB Atlas network access list
- **Authentication**: Username/password authentication required

---

## 🧪 Testing Guide

### Manual Testing with cURL

#### Test 1: Admin Workflow
```bash
# 1. Admin Signup
curl -X POST http://localhost:8000/admin-signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin1",
    "password": "admin123",
    "email": "admin@test.com",
    "role": "admin"
  }'

# 2. Admin Login (save the token)
curl -X POST http://localhost:8000/admin-login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin1",
    "password": "admin123"
  }'

# 3. Add Student (use token from step 2)
curl -X POST http://localhost:8000/admin-add-student \
  -H "Authorization: Bearer <ADMIN_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Alice Johnson",
    "age": 16,
    "roll_no": 201,
    "grade": "10"
  }'

# 4. Update Student
curl -X PUT http://localhost:8000/admin-update-student/1 \
  -H "Authorization: Bearer <ADMIN_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Alice Updated",
    "age": 17,
    "roll_no": 201,
    "grade": "11"
  }'

# 5. Delete Student
curl -X DELETE http://localhost:8000/admin-delete-student/1 \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

#### Test 2: User Workflow
```bash
# 1. User Signup
curl -X POST http://localhost:8000/user-signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "password": "user123",
    "email": "user@test.com",
    "role": "user"
  }'

# 2. User Login (save the token)
curl -X POST http://localhost:8000/user-login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "password": "user123"
  }'

# 3. View All Students (allowed)
curl -X GET http://localhost:8000/get-all-students \
  -H "Authorization: Bearer <USER_TOKEN>"

# 4. Try to Add Student (should fail with 403)
curl -X POST http://localhost:8000/admin-add-student \
  -H "Authorization: Bearer <USER_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 2,
    "name": "Bob",
    "age": 15,
    "roll_no": 202,
    "grade": "9"
  }'
# Expected: {"detail": "Access forbidden: Admin privileges required"}
```

#### Test 3: Search & Filter
```bash
# Filter by grade
curl -X GET "http://localhost:8000/students?grade=10" \
  -H "Authorization: Bearer <TOKEN>"

# Search by name
curl -X GET "http://localhost:8000/students?name=alice" \
  -H "Authorization: Bearer <TOKEN>"

# Search by roll number
curl -X GET "http://localhost:8000/students?roll_no=201" \
  -H "Authorization: Bearer <TOKEN>"

# Combine filters
curl -X GET "http://localhost:8000/students?grade=10&name=alice" \
  -H "Authorization: Bearer <TOKEN>"
```

### Testing with Postman

1. **Import Collection**: Create a new collection "FlowData API"
2. **Environment Variables**: Create variables for `base_url`, `admin_token`, `user_token`
3. **Test Sequence**:
   - Admin Signup → Admin Login → Save token
   - User Signup → User Login → Save token
   - Test admin operations with admin token
   - Test user operations with user token
   - Verify 403 errors when user tries admin operations

### Testing with Python
```python
import requests

BASE_URL = "http://localhost:8000"

# Admin Login
response = requests.post(f"{BASE_URL}/admin-login", json={
    "username": "admin1",
    "password": "admin123"
})
admin_token = response.json()["access_token"]

# Add Student
headers = {"Authorization": f"Bearer {admin_token}"}
response = requests.post(
    f"{BASE_URL}/admin-add-student",
    headers=headers,
    json={
        "id": 1,
        "name": "Test Student",
        "age": 15,
        "roll_no": 101,
        "grade": "9"
    }
)
print(response.json())
```

---

## ⚠️ Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful request |
| 400 | Bad Request | User already exists, invalid data |
| 401 | Unauthorized | Invalid/missing token |
| 403 | Forbidden | Insufficient privileges (role mismatch) |
| 404 | Not Found | User/Student not found |
| 422 | Unprocessable Entity | Validation error (Pydantic) |
| 500 | Internal Server Error | Server/database error |

### Common Error Responses

**401 Unauthorized**:
```json
{
  "detail": "Invalid or expired token"
}
```

**403 Forbidden**:
```json
{
  "detail": "Access forbidden: Admin privileges required"
}
```

**404 Not Found**:
```json
{
  "detail": "Student not found"
}
```

**400 Bad Request**:
```json
{
  "detail": "Admin already exists"
}
```

**422 Validation Error**:
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

---

## 🔧 Troubleshooting

### Issue: "Connection to MongoDB failed"
**Solution**:
- Check `MONGO_URI` in `.env` file
- Verify MongoDB Atlas network access (IP whitelist)
- Ensure database user has correct permissions
- Test connection with MongoDB Compass

### Issue: "Invalid or expired token"
**Solution**:
- Token may have expired (check `ACCESS_TOKEN_EXPIRE_MINUTES`)
- Login again to get a fresh token
- Ensure token is correctly copied (no extra spaces)
- Check that `SECRET_KEY` hasn't changed

### Issue: "403 Forbidden: Admin privileges required"
**Solution**:
- You're using a user token for an admin-only route
- Login as admin to get an admin token
- Verify token role claim in jwt.io

### Issue: "Package requirement not satisfied"
**Solution**:
```bash
pip install --upgrade -r requirements.txt
```

### Issue: "Module not found"
**Solution**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version (requires 3.12+)

### Issue: Port 8000 already in use
**Solution**:
```bash
# Run on different port
uvicorn main:app --reload --port 8001

# Or kill process on port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: CORS errors in browser
**Solution**:
- CORS is configured to allow all origins (`allow_origins=["*"]`)
- For production, specify exact origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 Best Practices

### For Admins
1. Use strong passwords (minimum 12 characters)
2. Rotate `SECRET_KEY` periodically
3. Set appropriate token expiration times
4. Monitor admin actions/logs
5. Limit admin accounts to necessary personnel

### For Developers
1. Never commit `.env` file to version control
2. Use environment-specific `.env` files (dev, staging, prod)
3. Implement rate limiting for production
4. Add request logging middleware
5. Use HTTPS in production
6. Implement refresh tokens for better UX
7. Add comprehensive error logging
8. Write unit and integration tests

### For Deployment
1. Use strong, random `SECRET_KEY`
2. Set `ACCESS_TOKEN_EXPIRE_MINUTES` appropriately
3. Configure CORS for specific origins
4. Enable MongoDB authentication
5. Use environment variables (not hardcoded values)
6. Set up monitoring and alerting
7. Regular database backups
8. Use HTTPS/TLS for all connections



