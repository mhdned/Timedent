from datetime import date, datetime, time
from typing import Optional

from fastapi import Form
from pydantic import BaseModel


class AvailableCourseDataForm(BaseModel):
    course_id: int
    teacher_id: int
    capacity: int
    start_time: time
    end_time: time
    start_date: date
    end_date: date

    @classmethod
    def get(
        cls,
        course_id: int = Form(...),
        teacher_id: int = Form(...),
        capacity: int = Form(...),
        start_time: time = Form(...),
        end_time: time = Form(...),
        start_date: date = Form(...),
        end_date: date = Form(...),
    ) -> "AvailableCourseDataForm":
        return cls(
            course_id=course_id,
            teacher_id=teacher_id,
            capacity=capacity,
            start_time=start_time,
            end_time=end_time,
            start_date=start_date,
            end_date=end_date,
        )


class AvailableCourseInfo(BaseModel):
    id: int
    course_id: int
    teacher_id: int
    capacity: int
    start_time: time
    end_time: time
    start_date: date
    end_date: date
    created_at: datetime
    updated_at: datetime


class AvailableCourseSearchForm(BaseModel):
    course_id: Optional[int]
    start_time: Optional[time]
    end_time: Optional[time]
    start_date: Optional[date]
    end_date: Optional[date]

    @classmethod
    def get(
        cls,
        course_id: Optional[int] = Form(None),
        start_time: Optional[time] = Form(None),
        end_time: Optional[time] = Form(None),
        start_date: Optional[date] = Form(None),
        end_date: Optional[date] = Form(None),
    ) -> "AvailableCourseSearchForm":
        return cls(
            course_id=course_id,
            start_time=start_time,
            end_time=end_time,
            start_date=start_date,
            end_date=end_date,
        )
