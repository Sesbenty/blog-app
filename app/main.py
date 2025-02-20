from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.adapters.orm import start_mappers
from app.routers.auth import auth_router
from app.routers.blog import blog_router
from app.routers.pages import frontend

app = FastAPI(title="Blog API")

start_mappers()


@app.get("/")
def root():
    return RedirectResponse("/feed")


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(blog_router)

app.include_router(frontend)
