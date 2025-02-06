from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from controllers.availalbe import AvailableCourseCRUD
from controllers.course import CourseCRUD
from controllers.field import FieldCRUD
from controllers.teacher import TeacherCRUD
from core.jinja import jinja
from dependencies import SessionDep
from middlewares.auth import auth_admin
from schemas.availalbe import AvailableCourseDataForm
from schemas.course import CourseDataForm

router = APIRouter()


@router.post(
    path="/add",
    description="Create new course for student",
    dependencies=[Depends(auth_admin)],
    status_code=status.HTTP_303_SEE_OTHER,
    response_class=RedirectResponse,
)
async def create_course(
    request: Request,
    db: SessionDep,
    course_form: CourseDataForm = Depends(CourseDataForm.get),
):
    course_crud = CourseCRUD(db)
    new_course = course_crud.create_course(course_form)

    if not new_course:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something wrong about storing data into database",
        )

    return RedirectResponse(
        url="/admin/dashboard/courses", status_code=status.HTTP_303_SEE_OTHER
    )


@router.get(
    path="/delete/{course_id}",
    response_class=RedirectResponse,
    description="Delete course from database (Hard Delete)",
    dependencies=[Depends(auth_admin)],
)
async def delete_course(
    course_id: int,
    request: Request,
    db: SessionDep,
    admin_info=Depends(auth_admin),
):
    course_crud = CourseCRUD(db)
    delete_course = course_crud.delete_course(course_id=course_id)

    if not delete_course:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The course may deleted before, or does not exists",
        )

    return RedirectResponse(
        url="/admin/dashboard/courses", status_code=status.HTTP_302_FOUND
    )


@router.get(
    path="/update/{course_id}",
    response_class=HTMLResponse,
    description="Update or modify field information",
    dependencies=[Depends(auth_admin)],
)
async def update_course_view(
    course_id: int, db: SessionDep, request: Request, admin_info=Depends(auth_admin)
):
    course_crud = CourseCRUD(session=db)
    course = course_crud.find_course_by_id(course_id)

    field_crud = FieldCRUD(db)
    fields = field_crud.find_fields()

    for field in fields:
        field["created_at"] = field["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        field["updated_at"] = field["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        field["deleted_at"] = None

    context = {"admin_info": admin_info, "course": course, "fields": fields}
    return jinja.response(
        request=request, name="admin/dashboard.course.edit.html", context=context
    )


@router.post(
    path="/update/{course_id}",
    response_class=RedirectResponse,
    description="Update or modify field information",
    dependencies=[Depends(auth_admin)],
)
async def update_course(
    course_id: int,
    db: SessionDep,
    request: Request,
    admin_info=Depends(auth_admin),
    course_form_data: CourseDataForm = Depends(CourseDataForm.get),
):
    course_crud = CourseCRUD(db)
    course = course_crud.find_course_by_id(course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The course does not found in database",
        )

    updated_course = course_crud.update_course_by_id(
        id=course_id, course_data=course_form_data
    )

    if not updated_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="course update failed with 400 status.",
        )

    return RedirectResponse(
        url="/admin/dashboard/courses", status_code=status.HTTP_302_FOUND
    )


@router.post(
    path="/available",
    response_class=RedirectResponse,
    dependencies=[Depends(auth_admin)],
    description="Create available course",
)
async def add_available(
    db: SessionDep,
    form_data: AvailableCourseDataForm = Depends(AvailableCourseDataForm.get),
):
    available_crud = AvailableCourseCRUD(db)
    new_ac = available_crud.create(form_data)

    if not new_ac:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something wrong about storing data into database",
        )

    return RedirectResponse(
        url="/admin/dashboard/available_courses", status_code=status.HTTP_302_FOUND
    )


@router.post(
    path="/available/delete/{ac_id}",
    response_class=RedirectResponse,
    dependencies=[Depends(auth_admin)],
    description="Delete available course",
)
async def add_available(
    ac_id: int,
    db: SessionDep,
    form_data: AvailableCourseDataForm = Depends(AvailableCourseDataForm.get),
):
    available_crud = AvailableCourseCRUD(db)
    delted_ac = available_crud.delete(ac_id)

    if not delted_ac:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something wrong about delete data from database",
        )

    return RedirectResponse(
        url="/admin/dashboard/available_courses", status_code=status.HTTP_302_FOUND
    )


@router.get(
    path="/available/update/{ac_id}",
    response_class=HTMLResponse,
    description="Update or modify available course information",
    dependencies=[Depends(auth_admin)],
)
async def update_course_view(
    ac_id: int, db: SessionDep, request: Request, admin_info=Depends(auth_admin)
):
    ac_crud = AvailableCourseCRUD(session=db)
    available_course = ac_crud.find_by_id(ac_id)
    
    available_course.start_date = available_course.start_date.strftime("%Y-%m-%d")
    available_course.end_date = available_course.end_date.strftime("%Y-%m-%d")
    
    available_course.start_time = available_course.start_time.strftime("%H:%M:%S")
    available_course.end_time = available_course.end_time.strftime("%H:%M:%S")
    
    available_course.created_at = available_course.created_at.strftime("%Y-%m-%d %H:%M:%S")
    available_course.updated_at = available_course.updated_at.strftime("%Y-%m-%d %H:%M:%S")

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
        

    context = {"admin_info": admin_info, "courses": courses, "available_course": available_course, "teachers" : teachers}
    return jinja.response(
        request=request, name="admin/dashboard.ac.edit.html", context=context
    )


@router.post(
    path="/available/update/{ac_id}",
    description="Modify action of available course",
    status_code=status.HTTP_303_SEE_OTHER,
    dependencies=[Depends(auth_admin)],
    response_class=RedirectResponse
)
async def update_available_course(
    ac_id: int,
    db: SessionDep,
    request: Request,
    admin_info= Depends(auth_admin),
    ac_form_data: AvailableCourseDataForm = Depends(AvailableCourseDataForm.get)
):
    ac_crud = AvailableCourseCRUD(db)
    ac_current = ac_crud.find_by_id(ac_id=ac_id)
    
    if not ac_current:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The available course may be deleted before or not exists"
        )
        
    ac_update = ac_crud.update_by_id(ac_id, ac_form_data)
    
    if not ac_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Something wrong about updating data in database"
        )
        
    return RedirectResponse(
        url="/admin/dashboard/available_courses", status_code=status.HTTP_302_FOUND
    )
        
    
