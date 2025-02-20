from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.domain.models.auth import User
from app.domain.models.blog import Blog
from app.domain.schemas.blog import BlogBase, BlogCreate, BlogInfo
from app.routes.dependecies import get_current_user, get_session

blog_router = APIRouter(prefix="/blog", tags=["Blog"])


@blog_router.delete("/{blog_id}")
async def delete_blog(
    blog_id: int,
    user_data: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    blog = session.get(Blog, blog_id)
    if blog.author_id == user_data.id:
        session.delete(blog)
        session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You are not the owner of the blog",
        )


@blog_router.get("/")
async def get_all_blogs(session: Session = Depends(get_session)):
    blogs = session.query(Blog).all()
    blogs_info = []
    for blog in blogs:
        blogs_info.append(BlogInfo.model_validate(asdict(blog)))
    return blogs_info


@blog_router.get("/{blog_id}")
async def get_blog(blog_id: int, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    blog_info = BlogInfo.model_validate(asdict(blog))
    return blog_info


@blog_router.post("/{blog_id}")
async def update_blog(
    blog_id: int,
    blog_data: BlogBase,
    user_data: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    blog_to_update = session.get(Blog, blog_id)
    if blog_to_update.author_id != user_data.id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You are not the owner of the blog",
        )

    blog_to_update.title = blog_data.title
    blog_to_update.body = blog_data.body
    session.commit()


@blog_router.post("/")
async def create_blog(
    blog_data: BlogCreate,
    user_data: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    blog = Blog(author_id=user_data.id, **blog_data.model_dump())
    session.add(blog)
    session.commit()
