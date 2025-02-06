# Import libraries, dependencies modules
from fastapi import Request


async def log_store_function(request: Request, call_next):
    response = await call_next(request)
    return response
