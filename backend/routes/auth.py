from fastapi import APIRouter
from datetime import datetime

from models.user import UserData
from database.db import users_collection
from utils.security import hash_password, verify_password, create_token
from utils.file_handler import create_user_folders

router = APIRouter()

@router.post("/signup")
def signup(user: UserData):

    email = user.email.strip().lower()

    if users_collection.find_one({"email": email}):
        return {"message": "User already exists"}

    users_collection.insert_one({
        "email": email,
        "password": hash_password(user.password),
        "created_at": datetime.utcnow()
    })

    create_user_folders(email)

    return {"message": "Signup successful"}


@router.post("/login")
def login(user: UserData):

    email = user.email.strip().lower()

    db_user = users_collection.find_one({"email": email})

    if not db_user:
        return {"message": "User not found"}

    if not verify_password(user.password, db_user["password"]):
        return {"message": "Invalid credentials"}

    token = create_token({"email": email})

    return {
        "message": "Login successful",
        "token": token
    }