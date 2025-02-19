from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 

from app.domain.models.auth import User
from app.domain.schemas.blog import BlogBase
from app.routes.dependecies import get_current_user, session_factory

blog_router = APIRouter(prefix="/blog", tags=["Blog"])


@blog_router.delete("/")
async def delete_blog():
    pass


@blog_router.get("/")
async def get_all_blogs():
    pass


@blog_router.get("/{blog_id}")
async def get_blog(blog_id: int):
    pass


@blog_router.post("/{blog_id}")
async def update_blog(blog_id: int):
    pass

async def create_blog(blod_data: BlogBase, user_data: User = Depends(get_current_user), session: Session = Depends(session_factory)):
    pass