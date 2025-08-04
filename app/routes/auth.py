from fastapi import APIRouter, HTTPException
from app.models.user import SignupModel, LoginModel
from app.utils.auth import hash_password, verify_password, create_id_token
from app.database import db
import uuid

router = APIRouter()

@router.post("/signup")
async def signup(user: SignupModel):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = f"user_{uuid.uuid4().hex[:8]}"  # example: user_1a2b3c4d
    user_dict = user.model_dump()
    user_dict["user_id"] = user_id
    user_dict["password"] = hash_password(user.password)

    await db.users.insert_one(user_dict)
    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "name": user.name,
        "email": user.email
    }

@router.post("/login")
async def login(user: LoginModel):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    id_token = create_id_token(data={"sub": user.email})

    return {
        "idToken": id_token,
        "user_id": db_user.get("user_id"),
        "name": db_user.get("name"),
        "email": db_user.get("email")
    }
