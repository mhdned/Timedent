# Import dependencies module
from pydantic import BaseModel


class LogCreateData(BaseModel):
    router: str
    ip: str
    body: str


class LogInfo(BaseModel):
    id: int
    router: str
    ip: str
    body: str


class LogAllResponse(BaseModel):
    message: str
    logs: list[LogInfo]
