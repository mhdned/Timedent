from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse

from core.jinja import jinja
from schemas.root import RootResponse

router = APIRouter()


@router.get(
    path="/check",
    status_code=status.HTTP_200_OK,
    description="This path is related to checking the execution of the application",
    response_class=JSONResponse,
    response_model=RootResponse,
)
async def root(request: Request):
    try:
        return {
            "message": "Timedent is alive.",
            "url": request.url.path,
            "method": request.method,
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    path="/",
    status_code=status.HTTP_303_SEE_OTHER,
    description="The main page of application",
    response_class=HTMLResponse,
)
async def home_view(request: Request):
    context = {}
    return jinja.response(request=request, name="home.html", context=context)
