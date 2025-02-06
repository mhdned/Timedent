from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from controllers.teacher import TeacherCRUD
from core.jinja import jinja
from dependencies import SessionDep
from middlewares.auth import auth_admin
from schemas.teacher import TeacherAddForm

router = APIRouter()


@router.post(
    path="/add",
    status_code=status.HTTP_303_SEE_OTHER,
    response_class=RedirectResponse,
    dependencies=[Depends(auth_admin)],
)
async def teacher_view(
    request: Request,
    db: SessionDep,
    admin_info=Depends(auth_admin),
    teacher_data_form: TeacherAddForm = Depends(TeacherAddForm.get),
):
    teacher_crud = TeacherCRUD(db)
    teacher = teacher_crud.create_teacher(teacher_data_form)

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong when application try to store teacher in database",
        )

    return RedirectResponse(
        url="/admin/dashboard/teachers", status_code=status.HTTP_303_SEE_OTHER
    )


@router.get(
    path="/delete/{teacher_id}",
    response_class=RedirectResponse,
    description="Delete single teacher with Id",
    dependencies=[Depends(auth_admin)],
)
async def delete_teacher(
    teacher_id: int,
    request: Request,
    db: SessionDep,
    admin_info=Depends(auth_admin),
):
    teacher_crud = TeacherCRUD(db)
    delete_teacher = teacher_crud.delete_teacher(teacher_id=teacher_id)

    if not delete_teacher:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The teacher may deleted before, or does not exists",
        )

    return RedirectResponse(
        url="/admin/dashboard/teachers", status_code=status.HTTP_302_FOUND
    )


@router.get(
    path="/update/{teacher_id}",
    response_class=HTMLResponse,
    description="Update or modify teacher information",
    dependencies=[Depends(auth_admin)],
)
async def update_teacher_view(
    teacher_id: int, db: SessionDep, request: Request, admin_info=Depends(auth_admin)
):
    teacher_crud = TeacherCRUD(session=db)
    teacher = teacher_crud.find_teacher_by_id(teacher_id)

    context = {"admin_info": admin_info, "teacher": teacher}
    return jinja.response(
        request=request, name="admin/dashboard.teacher.edit.html", context=context
    )


@router.post(
    path="/update/{teacher_id}",
    response_class=HTMLResponse,
    description="Update or modify teacher information",
    dependencies=[Depends(auth_admin)],
)
async def update_teacher(
    teacher_id: int,
    db: SessionDep,
    request: Request,
    admin_info=Depends(auth_admin),
    teacher_data_form: TeacherAddForm = Depends(TeacherAddForm.get),
):
    teacher_crud = TeacherCRUD(db)
    teacher = teacher_crud.find_teacher_by_id(teacher_id)

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The teacher does not found in database",
        )

    updated_teacher = teacher_crud.update_teacher_by_id(
        id=teacher_id, teacher_data=teacher_data_form
    )

    if not updated_teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="teacher update failed with 400 status.",
        )

    return RedirectResponse(
        url="/admin/dashboard/teachers", status_code=status.HTTP_302_FOUND
    )
