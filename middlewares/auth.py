# Import libraries, dependencies modules
from fastapi import HTTPException, Request, status

from controllers.auth import AuthCRUD
from dependencies import SessionDep
from utils.security import decode_access_token


async def auth_admin(db: SessionDep, request: Request):
    email = await decode_access_token(request=request)
    auth_crud = AuthCRUD(db)
    user_info = auth_crud.find_admin_by_email(email=email)

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You did not have credential to access this page",
        )

    return user_info


async def auth_client(db: SessionDep, request: Request):
    email = await decode_access_token(request=request)
    auth_crud = AuthCRUD(db)
    user_info = auth_crud.find_client_by_email(email=email)

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You did not have credential to access this page",
        )

    return user_info
