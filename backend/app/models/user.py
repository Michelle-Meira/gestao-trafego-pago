from pydantic import BaseModel, EmailStr, Field, ConfigDict, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    ANALYST = "analyst"
    VIEWER = "viewer"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=100)
    role: UserRole = UserRole.VIEWER
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)  # <-- Adicione max_length=72
    
    @validator('password')
    def validate_password_length(cls, v):
        if len(v) > 72:
            raise ValueError('Senha não pode ter mais de 72 caracteres')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3, max_length=100)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None
