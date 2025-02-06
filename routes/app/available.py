from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from controllers.availalbe import AvailableCourseCRUD
from core.jinja import jinja
from dependencies import SessionDep
from middlewares.auth import auth_client
from schemas.availalbe import AvailableCourseSearchForm

router = APIRouter()


@router.post(
    path="/search",
    description="search for find all course which that are match with student free time",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def search_course(
    request: Request,
    db: SessionDep,
    search_form: AvailableCourseSearchForm = Depends(AvailableCourseSearchForm.get),
):

    available_cours_crud = AvailableCourseCRUD(db)
    available_courses = available_cours_crud.find_filter(filter_param=search_form)

    available_courses_list: list[dict] = []

    for av_course in available_courses:
        temp_data = {
            "id": av_course.id,
            "course": av_course.course.subject,
            "teacher": f"{av_course.teacher.first_name} {av_course.teacher.last_name}",
            "capacity": av_course.capacity,
            "start_time": av_course.start_time.strftime("%H:%M:%S"),
            "end_time": av_course.end_time.strftime("%H:%M:%S"),
            "start_date": av_course.start_date.strftime("%Y-%m-%d"),
            "end_date": av_course.end_date.strftime("%Y-%m-%d"),
            "created_at": av_course.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": av_course.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

        available_courses_list.append(temp_data)

    context = {"available_courses": available_courses_list}
    return jinja.response(request=request, name="search.course.html", context=context)


@router.get(
    path="/elective/{ac_id}",
    description="elective available course",
    response_class=RedirectResponse,
    status_code=status.HTTP_303_SEE_OTHER,
)
async def elective_course(
    ac_id: int,
    request: Request,
    db: SessionDep,
    user_info=Depends(auth_client),
):

    ec_data = {"available_id": ac_id, "student_id": user_info.id}

    elective_course_crud = AvailableCourseCRUD(db)
    elective_course = elective_course_crud.elecrive_course_insert(ec_data)

    if not elective_course:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something wrong about storing data into data base",
        )

    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
