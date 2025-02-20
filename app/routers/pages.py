from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request

frontend = APIRouter(tags=["Frontend"])
tempalates = Jinja2Templates(directory="static/tempalates")


@frontend.get("/feed")
async def feed(request: Request):
    return tempalates.TemplateResponse(request=request, name="index.html", context={})


@frontend.get("/blogs/{blog_id}")
async def get_blog_page(blog_id):
    pass


@frontend.get("/user")
async def get_user_page():
    pass
