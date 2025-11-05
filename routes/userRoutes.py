from fastapi import APIRouter, HTTPException, Depends
from configuration.mongoDbConfig import db
from models.userModels import User, UserAuth
from passlib.context import CryptContext
from services.authentication import create_access_token, get_current_user


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#SIGNUP
@router.post("/user-signup")
def user_signup(user: User):
    existing_user = db.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
    user_doc = user.model_dump()
    user_doc["password"] = hashed_password
    user_doc["role"] = "user"  # Explicitly set role to 'user'
    db.users.insert_one(user_doc)
    return {"message": "User registered successfully", "username": user.username}

#LOGIN
@router.post("/user-login")
def user_login(auth: UserAuth):

    user = db.users.find_one({"username": auth.username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(auth.password, user.get("password", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    #default role to 'user' if not present
    access_token = create_access_token(data={"sub": auth.username, "role": user.get("role", "user")})
    user_safe = {k: v for k, v in user.items() if k not in ("password", "_id")}
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer", "user": user_safe}

