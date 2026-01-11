from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    hashed_password: str

class UserLogin(BaseModel):
    login: EmailStr | str
    password: str
