from fastapi import Depends, Form
from pydantic import BaseModel

from schemas.field import FieldData


class CourseDataForm(BaseModel):
    subject: str
    field_id: int

    @classmethod
    def get(
        cls, subject: str = Form(...), field_id: str = Form(...)
    ) -> "CourseDataForm":
        return cls(subject=subject, field_id=field_id)


class CourseInfo(BaseModel):
    id: int
    subject: str
    field_id: int
    field: FieldData
    field_title: str
