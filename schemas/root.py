from pydantic import BaseModel


class RootResponse(BaseModel):
    """
    Type:

    schama, extend from pydantic<BaseModel>

    Description:

    returns three json parameters which are (message, url, method).
    """

    message: str
    url: str
    method: str
