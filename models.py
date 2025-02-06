# Import built-in module
from datetime import datetime

# Import libraries, dependencies, packages module
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Time,
)
from sqlalchemy.orm import relationship

# Import post-built modules
from databases.connection import Base


class TimestampColumns:
    """
    Type:

    class, post-built, solution

    Description:

    Adding timestamps to database tables separately
    """

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)


class Log(Base, TimestampColumns):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    router = Column(String, index=True, nullable=False)
    ip = Column(String, nullable=False)
    body = Column(String, nullable=True)


class User(Base, TimestampColumns):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, nullable=False, default=False)

    electivecourses = relationship("ElectiveCourses", back_populates="student")


class Teacher(Base, TimestampColumns):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    available_course = relationship("AvailableCourses", back_populates="teacher")


class Field(Base, TimestampColumns):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, unique=True, nullable=False)

    course = relationship("Course", back_populates="field")


class Course(Base, TimestampColumns):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    subject = Column(String, unique=True, nullable=False)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)

    field = relationship("Field", back_populates="course")
    available_course = relationship("AvailableCourses", back_populates="course")


class AvailableCourses(Base, TimestampColumns):
    __tablename__ = "available_course"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    capacity = Column(
        Integer,
        CheckConstraint("capacity >= 5 AND capacity <= 30"),
        default=15,
        nullable=False,
    )
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    course = relationship("Course", back_populates="available_course")
    teacher = relationship("Teacher", back_populates="available_course")
    electivecourses = relationship("ElectiveCourses", back_populates="available")


class ElectiveCourses(Base, TimestampColumns):
    __tablename__ = "elective_course"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    available_id = Column(Integer, ForeignKey("available_course.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(
        Integer, CheckConstraint("score >= 0 AND score <= 20"), nullable=True
    )

    available = relationship("AvailableCourses", back_populates="electivecourses")
    student = relationship("User", back_populates="electivecourses")
