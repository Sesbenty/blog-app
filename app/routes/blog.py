from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.domain.models.auth import User
from app.domain.models.blog import Blog
from app.domain.schemas.blog import BlogBase
from app.routes.dependecies import get_current_user, get_session

blog_router = APIRouter(prefix="/blog", tags=["Blog"])


@blog_router.delete("/")
async def delete_blog():
    pass


@blog_router.get("/")
async def get_all_blogs():
    pass


@blog_router.get("/{blog_id}")
async def get_blog(blog_id: int, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    # blog_info = BlogInfo.model_validate(asdict(blog))
    return blog


@blog_router.post("/{blog_id}")
async def update_blog(
    blog_id: int,
    blog_data: BlogBase,
    user_data: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    blog_to_update = session.get(Blog, blog_id)
    if blog_to_update.author_id != user_data.id:
        raise HTTPException()

    blog_to_update.title = blog_data.title
    blog_to_update.body = blog_data.body
    session.commit()


@blog_router.post("/")
async def create_blog(
    blog_data: BlogBase,
    user_data: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    blog = Blog(author_id=user_data.id, **blog_data.model_dump())
    session.add(blog)
    session.commit()
