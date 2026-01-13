from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    hashed_password: str

class UserLogin(BaseModel):
    login: EmailStr | str
    password: str

# Schemas for API's endpoints
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
