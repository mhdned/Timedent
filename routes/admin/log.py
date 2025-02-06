# Import libraries modules
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from controllers.log import LogCRUD

# Import post-built modules
from dependencies import SessionDep
from schemas.log import LogAllResponse

# Create instance of APIRouter
router = APIRouter()

# Definition routes


@router.get(
    path="/",
    description="Response all logs which store in our database",
    response_class=JSONResponse,
    response_model=LogAllResponse,
    status_code=status.HTTP_200_OK,
)
async def log_all(db: SessionDep):
    log_crud = LogCRUD(session=db)
    log_read_all = await log_crud.read_all()

    if not log_read_all:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found any log in database storage",
        )

    return {"message": "all logs founded successfully", "logs": log_read_all}
