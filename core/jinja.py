# import jinja
from fastapi import Request
from fastapi.templating import Jinja2Templates

# pointed to templates
templates = Jinja2Templates(directory="templates")


# jinja class
class JinjaTemplateEngine:

    def __init__(self) -> None:
        pass

    def response(self, request: Request, name: str, context):
        return templates.TemplateResponse(request=request, name=name, context=context)


jinja = JinjaTemplateEngine()
