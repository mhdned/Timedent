from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from controllers.field import FieldCRUD
from core.jinja import jinja
from dependencies import SessionDep
from middlewares.auth import auth_admin
from schemas.field import FieldFormData

router = APIRouter()


@router.post(
    path="/add",
    response_class=RedirectResponse,
    dependencies=[Depends(auth_admin)],
    description="create field",
    status_code=status.HTTP_303_SEE_OTHER,
)
async def add_field(
    request: Request,
    db: SessionDep,
    field_form_data: FieldFormData = Depends(FieldFormData.get),
):
    field_Crud = FieldCRUD(db)
    new_field = field_Crud.create_field(field_form_data)

    if not new_field:
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong about storing field data into database",
        )

    return RedirectResponse(
        url="/admin/dashboard/fields", status_code=status.HTTP_303_SEE_OTHER
    )


@router.get(
    path="/delete/{field_id}",
    dependencies=[Depends(auth_admin)],
    description="delete a single field from application",
    response_class=RedirectResponse,
    status_code=status.HTTP_303_SEE_OTHER,
)
async def delete_field(field_id: int, request: Request, db: SessionDep):
    field_crud = FieldCRUD(session=db)
    delete_field = field_crud.delete_field(field_id=field_id)

    if not delete_field:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The field may deleted before, or does not exists",
        )

    return RedirectResponse(
        url="/admin/dashboard/fields", status_code=status.HTTP_302_FOUND
    )


@router.get(
    path="/update/{field_id}",
    response_class=HTMLResponse,
    description="Update or modify field information",
    dependencies=[Depends(auth_admin)],
)
async def update_teacher_view(
    field_id: int, db: SessionDep, request: Request, admin_info=Depends(auth_admin)
):
    field_crud = FieldCRUD(session=db)
    field = field_crud.find_field_by_id(field_id)

    context = {"admin_info": admin_info, "field": field}
    return jinja.response(
        request=request, name="admin/dashboard.field.edit.html", context=context
    )


@router.post(
    path="/update/{field_id}",
    response_class=RedirectResponse,
    description="Update or modify teacher information",
    dependencies=[Depends(auth_admin)],
)
async def update_teacher(
    field_id: int,
    db: SessionDep,
    request: Request,
    admin_info=Depends(auth_admin),
    field_form_data: FieldFormData = Depends(FieldFormData.get),
):
    field_crud = FieldCRUD(db)
    field = field_crud.find_field_by_id(field_id)

    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The field does not found in database",
        )

    updated_field = field_crud.update_field_by_id(
        id=field_id, field_data=field_form_data
    )

    if not updated_field:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="field update failed with 400 status.",
        )

    return RedirectResponse(
        url="/admin/dashboard/fields", status_code=status.HTTP_302_FOUND
    )
