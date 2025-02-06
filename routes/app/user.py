from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from controllers.user import UserCRUD
from core.jinja import jinja
from dependencies import SessionDep
from middlewares.auth import auth_admin
from schemas.user import UserUpdateForm

router = APIRouter()


@router.get(
    path="/delete/{user_id}",
    response_class=RedirectResponse,
    description="Delete single user with Id",
    dependencies=[Depends(auth_admin)],
)
async def delete_user(
    user_id: int,
    request: Request,
    db: SessionDep,
    admin_info=Depends(auth_admin),
):
    user_crud = UserCRUD(db)
    delete_user = user_crud.delete_user(user_id=user_id)

    if not delete_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The user may deleted before, or does not exists",
        )

    return RedirectResponse(
        url="/admin/dashboard/users", status_code=status.HTTP_302_FOUND
    )


@router.get(
    path="/update/{user_id}",
    response_class=HTMLResponse,
    description="Update or modify user information",
    dependencies=[Depends(auth_admin)],
)
async def update_user_view(
    user_id: int, db: SessionDep, request: Request, admin_info=Depends(auth_admin)
):
    user_crud = UserCRUD(session=db)
    user = user_crud.find_user_by_id(id=user_id)

    context = {"admin_info": admin_info, "user": user}
    return jinja.response(
        request=request, name="admin/dashboard.user.edit.html", context=context
    )


@router.post(
    path="/update/{user_id}",
    response_class=RedirectResponse,
    description="Update or modify user information",
    dependencies=[Depends(auth_admin)],
    status_code=status.HTTP_302_FOUND,
)
async def update_user(
    user_id: int,
    db: SessionDep,
    request: Request,
    admin_info=Depends(auth_admin),
    user_data_form: UserUpdateForm = Depends(UserUpdateForm.get),
):
    user_crud = UserCRUD(db)
    user = user_crud.find_user_by_id(id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not found in database",
        )

    updated_user = user_crud.update_user_by_id(id=user_id, user_data=user_data_form)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user update failed with 400 status.",
        )

    return RedirectResponse(
        url="/admin/dashboard/users", status_code=status.HTTP_302_FOUND
    )
