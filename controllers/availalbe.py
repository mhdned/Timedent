from sqlalchemy import and_, between
from sqlalchemy.orm import Session

from models import AvailableCourses, Course, ElectiveCourses, Teacher, User
from schemas.availalbe import (
    AvailableCourseDataForm,
    AvailableCourseInfo,
    AvailableCourseSearchForm,
)
from utils.database import to_dict


class AvailableCourseCRUD:

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, available_data: AvailableCourseDataForm) -> AvailableCourseInfo:
        new_course = AvailableCourses(
            course_id=available_data.course_id,
            teacher_id=available_data.teacher_id,
            capacity=available_data.capacity,
            start_time=available_data.start_time,
            end_time=available_data.end_time,
            start_date=available_data.start_date,
            end_date=available_data.end_date,
        )

        self.session.add(new_course)
        self.session.commit()
        self.session.refresh(new_course)

        return new_course

    def find_by_id(self, ac_id: int) -> AvailableCourseInfo:
        return (
            self.session.query(AvailableCourses)
            .filter(AvailableCourses.id == ac_id)
            .first()
        )

    def find_available(self) -> list[dict]:
        courses = self.session.query(AvailableCourses).join(Course).join(Teacher).all()

        courses_result: list[dict] = []

        for course in courses:
            course_temp = {
                "id": course.id,
                "course": course.course.subject,
                "teacher": f"{course.teacher.first_name} {course.teacher.last_name}",
                "capacity": course.capacity,
                "start_date": course.start_date,
                "end_date": course.end_date,
                "start_time": course.start_time,
                "end_time": course.end_time,
                "created_at": course.created_at,
                "updated_at": course.updated_at,
                "deleted_at": course.deleted_at,
            }

            courses_result.append(course_temp)

        return courses_result

    def delete(self, ac_id: int) -> bool:
        find_course = (
            self.session.query(AvailableCourses)
            .filter(AvailableCourses.id == ac_id)
            .first()
        )

        if not find_course:
            return False
        else:
            self.session.delete(find_course)
            self.session.commit()
        return True

    def update_by_id(
        self, id: int, ac_data: AvailableCourseDataForm
    ) -> AvailableCourseInfo:
        course = (
            self.session.query(AvailableCourses)
            .filter(AvailableCourses.id == id)
            .one_or_none()
        )
        new_data = {
            "course_id": (
                ac_data.course_id if ac_data.course_id is not None else course.course_id
            ),
            "teacher_id": (
                ac_data.teacher_id
                if ac_data.teacher_id is not None
                else course.teacher_id
            ),
            "capacity": (
                ac_data.capacity if ac_data.capacity is not None else course.capacity
            ),
            "start_time": (
                ac_data.start_time
                if ac_data.start_time is not None
                else course.start_time
            ),
            "end_time": (
                ac_data.end_time if ac_data.end_time is not None else course.end_time
            ),
            "start_date": (
                ac_data.start_date
                if ac_data.start_date is not None
                else course.start_date
            ),
            "end_date": (
                ac_data.end_date if ac_data.end_date is not None else course.end_date
            ),
        }
        for key, value in new_data.items():
            setattr(course, key, value)
        self.session.commit()

        return course

    def find_filter(self, filter_param: AvailableCourseSearchForm) -> list:
        # Start with a query on the AvailableCourses model
        query = self.session.query(AvailableCourses)

        # Build a list of filter conditions
        filter_conditions = []

        # Handle each attribute in filter_param
        if filter_param.course_id is not None:
            filter_conditions.append(
                AvailableCourses.course_id == filter_param.course_id
            )

        if filter_param.start_time is not None and filter_param.end_time is not None:
            filter_conditions.append(
                between(
                    AvailableCourses.start_time,
                    filter_param.start_time,
                    filter_param.end_time,
                )
            )
        elif filter_param.start_time is not None:
            filter_conditions.append(
                AvailableCourses.start_time >= filter_param.start_time
            )
        elif filter_param.end_time is not None:
            filter_conditions.append(
                AvailableCourses.start_time <= filter_param.end_time
            )

        if filter_param.start_date is not None and filter_param.end_date is not None:
            filter_conditions.append(
                between(
                    AvailableCourses.start_date,
                    filter_param.start_date,
                    filter_param.end_date,
                )
            )
        elif filter_param.start_date is not None:
            filter_conditions.append(
                AvailableCourses.start_date >= filter_param.start_date
            )
        elif filter_param.end_date is not None:
            filter_conditions.append(
                AvailableCourses.start_date <= filter_param.end_date
            )

        # Apply all filter conditions to the query
        if filter_conditions:
            query = query.filter(and_(*filter_conditions))

        # Execute the query and return the results
        return query.all()

    def elecrive_course_insert(self, elective_info: dict):
        new_course = ElectiveCourses(
            available_id=elective_info["available_id"],
            student_id=elective_info["student_id"],
        )

        self.session.add(new_course)
        self.session.commit()
        self.session.refresh(new_course)

        return new_course

    def find_elective(self) -> list[dict]:
        courses = (
            self.session.query(ElectiveCourses)
            .join(AvailableCourses)
            .join(User)
            .join(Course, AvailableCourses.course_id)
            .all()
        )

        courses_result: list[dict] = []

        for course in courses:

            course_temp = {
                "id": course.id,
                "available": course.available.subject,
                "student": f"{course.teacher.username}",
                "updated_at": course.updated_at,
                "deleted_at": course.deleted_at,
            }

            courses_result.append(course_temp)

        return courses_result
