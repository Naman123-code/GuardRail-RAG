
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    tenant_id: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AskQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=2000)