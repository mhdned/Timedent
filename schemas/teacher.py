from fastapi import Form
from pydantic import BaseModel


class TeacherAddForm(BaseModel):
    firstname: str
    lastname: str

    @classmethod
    def get(
        cls,
        firstname: str = Form(...),
        lastname: str = Form(...),
    ) -> "TeacherAddForm":
        return cls(firstname=firstname, lastname=lastname)


class TeacherData(BaseModel):
    id: int
    first_name: str
    last_name: str
