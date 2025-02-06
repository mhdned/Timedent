# Import libraries, dependencies, packages modules
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_404_NOT_FOUND

# Create instance of application
app = FastAPI()

# Import post-built modules
from configs.config import config
from core.jinja import jinja
from middlewares.log import log_store_function
from routes.admin.index import router as AdminRouter
from routes.index import router as IndexRouter

# Log store middleware, run before all http requests
app.middleware("http")(log_store_function)

# jinja static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Includes all application routes
app.include_router(router=IndexRouter, prefix="", tags=["APPLICATION"])
app.include_router(router=AdminRouter, prefix="/admin", tags=["ADMIN"])


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == HTTP_404_NOT_FOUND:
        return jinja.response(request=request, name="error/404.html", context={})
    return HTMLResponse(content=str(exc.detail), status_code=exc.status_code)


# Configure Uvicorn to run the application
if __name__ == "__main__":
    uvicorn.run(app=app, host=config.HOST, port=config.PORT)
