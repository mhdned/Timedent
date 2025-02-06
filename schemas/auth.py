from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, EmailStr


class AuthLoginAdminForm(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def get(
        cls,
        password: str = Form(...),
        email: EmailStr = Form(...),
    ) -> "AuthLoginAdminForm":
        return cls(password=password, email=email)


class AuthLoginClientForm(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def get(
        cls,
        password: str = Form(...),
        email: EmailStr = Form(...),
    ) -> "AuthLoginClientForm":
        return cls(password=password, email=email)


class AuthRegisterClientForm(BaseModel):
    email: EmailStr
    username: str
    password: str

    @classmethod
    def get(
        cls,
        password: str = Form(...),
        email: EmailStr = Form(...),
        username: str = Form(...),
    ) -> "AuthRegisterClientForm":
        return cls(password=password, email=email, username=username)


class AuthAdminInfo(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    is_admin: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class AuthUserInfo(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class AuthCreateClientData(BaseModel):
    username: str
    email: EmailStr
    password: str
