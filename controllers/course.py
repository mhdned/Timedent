from sqlalchemy.orm import Session, joinedload

from models import Course, Field
from schemas.course import CourseDataForm, CourseInfo
from utils.database import to_dict


class CourseCRUD:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_courses(self) -> list[dict]:
        courses = self.session.query(Course).join(Field).all()

        courses_result: list[dict] = []

        for course in courses:
            course_temp = {
                "id": course.id,
                "subject": course.subject,
                "field_id": course.field.id,
                "field_title": course.field.title,
                "created_at": course.created_at,
                "updated_at": course.updated_at,
                "deleted_at": course.deleted_at,
            }

            courses_result.append(course_temp)

        return courses_result

    def find_course_by_id(self, course_id: int) -> CourseInfo:
        return self.session.query(Course).filter(Course.id == course_id).first()

    def create_course(self, course_data: CourseDataForm) -> CourseInfo:
        new_course = Course(subject=course_data.subject, field_id=course_data.field_id)

        self.session.add(new_course)
        self.session.commit()
        self.session.refresh(new_course)

        return new_course

    def delete_course(self, course_id: int) -> bool:
        find_course = self.session.query(Course).filter(Course.id == course_id).first()

        if not find_course:
            return False
        else:
            self.session.delete(find_course)
            self.session.commit()
        return True

    def update_course_by_id(self, id: int, course_data: CourseDataForm) -> CourseInfo:
        course = self.session.query(Course).filter(Course.id == id).one_or_none()
        new_data = {
            "subject": (
                course_data.subject
                if course_data.subject is not None
                else course.subject
            ),
            "field_id": (
                course_data.field_id
                if course_data.field_id is not None
                else course.field_id
            ),
        }
        for key, value in new_data.items():
            setattr(course, key, value)
        self.session.commit()

        return course
