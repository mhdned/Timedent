from datetime import datetime

from fastapi import Form
from pydantic import BaseModel


class FieldData(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime


class FieldFormData(BaseModel):
    title: str

    @classmethod
    def get(cls, title: str = Form(...)) -> "FieldFormData":
        return cls(title=title)
