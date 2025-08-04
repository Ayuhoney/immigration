from fastapi import APIRouter, HTTPException, Depends
from app.models.user_info import UserPersonalInfo,UserIdRequest
from app.database import db
from app.utils.auth import get_current_user
from datetime import date


router = APIRouter(
    prefix="/userInfo",
    tags=["userInfo"],
    dependencies=[Depends(get_current_user)]
)

# ✅ Save user personal info
@router.post("/submit")
async def submit_user_info(info: UserPersonalInfo):
    user = await db.users.find_one({"user_id": info.user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = await db.user_info.find_one({"user_id": info.user_id})
    if existing:
        raise HTTPException(status_code=400, detail="User info already exists")

    # Convert Pydantic model to dict
    data = info.model_dump()

    # ✅ Convert all `date` objects to ISO string
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = value.isoformat()  # 'YYYY-MM-DD'

    await db.user_info.insert_one(data)
    return {"message": "User personal info saved successfully", "user_id": info.user_id}



@router.post("/userdetails")
async def get_user_info(payload: UserIdRequest):
    user_id = payload.user_id

    # 1. Fetch personal info
    user_info = await db.user_info.find_one({"user_id": user_id})
    if user_info:
        user_info["_id"] = str(user_info["_id"])
    else:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Return result
    return {
        "user_info": user_info
    }