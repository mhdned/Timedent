from sqlalchemy.orm import Session

from models import Teacher
from schemas.teacher import TeacherAddForm, TeacherData
from utils.database import to_dict


class TeacherCRUD:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_teachers(self) -> list[dict]:
        teachers = self.session.query(Teacher).filter().all()
        teachers_list = [to_dict(teacher) for teacher in teachers]
        return teachers_list

    def find_teacher_by_id(self, teacher_id: int) -> TeacherData:
        return self.session.query(Teacher).filter(Teacher.id == teacher_id).first()

    def create_teacher(self, teacher_data: TeacherAddForm):
        teacher = Teacher(
            first_name=teacher_data.firstname,
            last_name=teacher_data.lastname,
        )
        self.session.add(teacher)
        self.session.commit()
        self.session.refresh(teacher)

        return teacher

    def delete_teacher(self, teacher_id: int) -> bool:

        teacher = self.session.query(Teacher).filter(Teacher.id == teacher_id).first()
        if teacher:
            self.session.delete(teacher)
            self.session.commit()
        else:
            return False
        return True

    def update_teacher_by_id(
        self, id: int, teacher_data: TeacherAddForm
    ) -> TeacherData:
        teacher = self.session.query(Teacher).filter(Teacher.id == id).one_or_none()

        new_data = {
            "first_name": (
                teacher_data.firstname
                if teacher_data.firstname is not None
                else teacher.first_name
            ),
            "last_name": (
                teacher_data.lastname
                if teacher_data.lastname is not None
                else teacher.last_name
            ),
        }

        for key, value in new_data.items():
            setattr(teacher, key, value)
        self.session.commit()
        return teacher
