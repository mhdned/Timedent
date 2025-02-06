from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse

from controllers.course import CourseCRUD
from core.jinja import jinja
from dependencies import SessionDep

router = APIRouter()


@router.get(
    path="/",
    response_class=HTMLResponse,
    description="Client dashboard panel",
    status_code=status.HTTP_200_OK,
)
async def dashboard_view(request: Request, db: SessionDep):

    cours_crud = CourseCRUD(db)
    courses = cours_crud.find_courses()

    for course in courses:
        course["created_at"] = course["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        course["updated_at"] = course["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        course["deleted_at"] = None

    context = {"courses": courses}
    return jinja.response(request=request, name="dashboard.html", context=context)
