from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse

from controllers.availalbe import AvailableCourseCRUD
from controllers.course import CourseCRUD
from controllers.field import FieldCRUD
from controllers.teacher import TeacherCRUD
from controllers.user import UserCRUD
from core.jinja import jinja
from dependencies import SessionDep
from middlewares.auth import auth_admin
from schemas.auth import AuthAdminInfo

router = APIRouter()


@router.get(
    path="/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="main dashboard of admin",
)
async def dashboard_view(
    request: Request, admin_info: AuthAdminInfo = Depends(auth_admin)
):

    context = {"admin_info": admin_info, "page": "dashboard"}
    return jinja.response(request=request, name="admin/dashboard.html", context=context)


@router.get(
    path="/users",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="main dashboard of admin",
)
async def dashboard_view(
    request: Request, db: SessionDep, admin_info: AuthAdminInfo = Depends(auth_admin)
):
    # find all users
    user_crud = UserCRUD(db)
    users = user_crud.find_users()

    for user in users:
        user["created_at"] = user["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        user["updated_at"] = user["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        user["deleted_at"] = None
        user["delete_link"] = f"/user/delete/{user["id"]}"

    context = {"admin_info": admin_info, "page": "users", "users": users}
    return jinja.response(
        request=request, name="admin/dashboard.users.html", context=context
    )


@router.get(
    path="/teachers",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    dependencies=[Depends(auth_admin)],
)
async def teacher_view(
    request: Request, db: SessionDep, admin_info: AuthAdminInfo=Depends(auth_admin)
):
        # find all users
    teacher_crud = TeacherCRUD(db)
    teachers = teacher_crud.find_teachers()

    for teacher in teachers:
        teacher["created_at"] = teacher["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        teacher["updated_at"] = teacher["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        teacher["deleted_at"] = None
    
    context: dict = {"admin_info" : admin_info,  "page": "teachers", "teachers": teachers}
    return jinja.response(
        request=request, name="admin/dashboard.teacher.html", context=context
    )
    
@router.get(
    path="/fields",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    dependencies=[Depends(auth_admin)],
)
async def field_view(
    request: Request, db: SessionDep, admin_info: AuthAdminInfo=Depends(auth_admin)
):

    field_crud = FieldCRUD(db)
    fields = field_crud.find_fields()
    
    for field in fields:
        field["created_at"] = field["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        field["updated_at"] = field["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        field["deleted_at"] = None
    
    context: dict = {"admin_info" : admin_info,  "page": "fields", "fields": fields}
    return jinja.response(
        request=request, name="admin/dashboard.field.html", context=context
    )
    
@router.get(
    path="/courses",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    dependencies=[Depends(auth_admin)],
)
async def course_view(
    request: Request, db: SessionDep, admin_info: AuthAdminInfo=Depends(auth_admin)
):
    field_crud = FieldCRUD(db)
    fields = field_crud.find_fields()
    
    for field in fields:
        field["created_at"] = field["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        field["updated_at"] = field["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        field["deleted_at"] = None
        
    course_crud = CourseCRUD(db)
    courses = course_crud.find_courses()
    
    for course in courses:
        course["created_at"] = course["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        course["updated_at"] = course["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        course["deleted_at"] = None
    
    context: dict = {
        "admin_info" : admin_info,  
        "page": "courses", 
        "fields" : fields, 
        "courses" : courses
    }
    
    return jinja.response(
        request=request, name="admin/dashboard.course.html", context=context
    )


@router.get(
    path="/available_courses",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_admin)],
    description="available course section"
)
async def available_course_view(request: Request, db: SessionDep, admin_info: AuthAdminInfo=Depends(auth_admin)):
    
    course_crud = CourseCRUD(db)
    courses = course_crud.find_courses()
    
    for course in courses:
        course["created_at"] = course["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        course["updated_at"] = course["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        course["deleted_at"] = None
        
    teacher_crud = TeacherCRUD(db)
    teachers = teacher_crud.find_teachers()
    
    for teacher in teachers:
        teacher["fullname"] = f"{teacher["first_name"]} {teacher["last_name"]}"
        teacher["created_at"] = teacher["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        teacher["updated_at"] = teacher["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        teacher["deleted_at"] = None
        
    
    available_crud = AvailableCourseCRUD(db)
    availables = available_crud.find_available()
    
    for available in availables:
        available["start_date"] = available["start_date"].strftime("%Y-%m-%d")
        available["end_date"] = available["end_date"].strftime("%Y-%m-%d")
        
        available["start_time"] = available["start_time"].strftime("%H:%M:%S")
        available["end_time"] = available["end_time"].strftime("%H:%M:%S")
        
        available["created_at"] = available["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        available["updated_at"] = available["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        available["deleted_at"] = None
    
    context = {
        "admin_info" : admin_info, 
        "page": "available_courses",
        "teachers" : teachers,
        "courses" : courses,
        "availables" : availables
    }
    return jinja.response(request=request,name="admin/dashboard.ac.html", context=context)


@router.get(
    path="/elective_courses",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    dependencies=[Depends(auth_admin)],
)
async def course_view(
    request: Request, db: SessionDep, admin_info: AuthAdminInfo=Depends(auth_admin)
):
    field_crud = FieldCRUD(db)
    fields = field_crud.find_fields()
    
    for field in fields:
        field["created_at"] = field["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        field["updated_at"] = field["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        field["deleted_at"] = None
        
    course_crud = CourseCRUD(db)
    courses = course_crud.find_courses()
    
    for course in courses:
        course["created_at"] = course["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        course["updated_at"] = course["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        course["deleted_at"] = None
    
    context: dict = {
        "admin_info" : admin_info,  
        "page": "courses", 
        "fields" : fields, 
        "courses" : courses
    }
    
    return jinja.response(
        request=request, name="admin/dashboard.course.html", context=context
    )
