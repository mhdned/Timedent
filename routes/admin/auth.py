# Import libraries modules
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from controllers.auth import AuthCRUD
from core.jinja import jinja
from dependencies import SessionDep
from schemas.auth import AuthLoginAdminForm
from utils.security import compare_passwords, create_access_token

router = APIRouter()


@router.get(
    path="/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    description="Admin section for login",
)
def admin_auth(request: Request):
    context = {}
    return jinja.response(
        request=request, name="auth/admin.login.html", context=context
    )


@router.post(
    path="/",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
    description="Admin authentication action route",
)
def admin_auth_action(
    request: Request,
    db: SessionDep,
    login_form: AuthLoginAdminForm = Depends(AuthLoginAdminForm.get),
):
    auth_crud = AuthCRUD(session=db)
    admin_info = auth_crud.find_admin_by_email(email=login_form.email)
    if not admin_info:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="authentication admin failed",
        )

    if not admin_info.is_admin:
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User is not admin, dont try again to entrance dude :(",
        )

    if not compare_passwords(login_form.password, admin_info.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The sent password is wrong",
        )
    access_token = create_access_token({"email": admin_info.email})

    response = RedirectResponse(
        url="/admin/dashboard", status_code=status.HTTP_302_FOUND
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response
