from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.auth import auth_router
from app.routes.blog import blog_router

app = FastAPI(title="Blog API")


@app.get("/")
def root():
    return "root"


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(blog_router)
