from pydantic import BaseModel, field_validator
from typing import Optional
import re

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) > 72:
            raise ValueError('Password must not exceed 72 characters')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) > 72:
            raise ValueError('Password must not exceed 72 characters')
        return v

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True