from datetime import datetime
from typing import Annotated, Any, Optional

from fastapi import Form
from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdateData(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdateForm(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]

    @classmethod
    def get(
        cls,
        email: Optional[EmailStr] = Form(...),
        username: Optional[str] = Form(...),
    ) -> "UserUpdateForm":
        return cls(email=email, username=username)
