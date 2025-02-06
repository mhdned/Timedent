from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from controllers.auth import AuthCRUD
from core.jinja import jinja
from dependencies import SessionDep
from schemas.auth import AuthLoginClientForm, AuthRegisterClientForm
from utils.security import (compare_passwords, create_access_token,
                            hash_password)

router = APIRouter()


@router.get(
    path="/register",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    description="Register page for regular client",
)
async def register_view(request: Request):

    context: dict = {}
    return jinja.response(request=request, name="auth/register.html", context=context)


@router.post(
    path="/register",
    status_code=status.HTTP_302_FOUND,
    response_class=RedirectResponse,
    description="Register endpoint for regular client",
)
async def register_client(
    request: Request,
    db: SessionDep,
    client_info: AuthRegisterClientForm = Depends(AuthRegisterClientForm.get),
):
    client_info.password = hash_password(client_info.password)
    auth_crud = AuthCRUD(db)
    inserted_client = auth_crud.create_client(client_data=client_info)

    if not inserted_client:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong about storing data to database, please try register account again ot contact support",
        )

    return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)


@router.get(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    description="Login page for regular client",
)
async def login_view(request: Request):
    context: dict = {}
    return jinja.response(request=request, name="auth/login.html", context=context)


@router.post(
    path="/login",
    status_code=status.HTTP_302_FOUND,
    response_class=RedirectResponse,
    description="Login endpoint for regular client",
)
async def login_client(
    request: Request,
    db: SessionDep,
    client_info: AuthLoginClientForm = Depends(AuthLoginClientForm.get),
):
    auth_crud = AuthCRUD(db)
    client = auth_crud.find_client_by_email(client_info.email)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client does not exist in database",
        )

    if not compare_passwords(client_info.password, client.password):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The password is wrong"
        )

    access_token = create_access_token({"email": client.email})

    response = RedirectResponse(
        url=f"/dashboard", status_code=status.HTTP_302_FOUND
    )
    response.set_cookie(key="access_token", value=access_token)

    return response
