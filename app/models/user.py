from pydantic import BaseModel, EmailStr

class SignupModel(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    name: str
    email: EmailStr
    password: str  # hashed
