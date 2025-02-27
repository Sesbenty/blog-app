from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, status

from app.adapters.repository import BlogRepository
from app.domain.schemas.blog import (
    BlogBase,
    BlogCreate,
    BlogInfo,
    CommentCreate,
    CommentUpdate,
)
from app.routers.dependecies import get_blog_repository, get_uow, get_user_id
from app.service_layer import services
from app.service_layer.exceptions import ServicesException
from app.service_layer.unit_of_work import AbstractUnitOfWork

blog_router = APIRouter(prefix="/blog", tags=["Blog"])


@blog_router.delete("/{blog_id}")
async def delete_blog(
    blog_id: int,
    user_id: int = Depends(get_user_id),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    try:
        services.delete_blog(blog_id, user_id, uow)
    except ServicesException as e:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Method not allowed: {str(e)}",
        )


@blog_router.get("/")
async def get_blogs(page_count: int):
    pass


@blog_router.get("/{blog_id}")
async def get_blog(blog_id: int, repo: BlogRepository = Depends(get_blog_repository)):
    blog = repo.get(blog_id)
    if blog:
        blog_info = BlogInfo.model_validate(asdict(blog))
        return blog_info
    else:
        pass


@blog_router.put("/{blog_id}")
async def update_blog(
    blog_id: int,
    blog_data: BlogBase,
    user_id: int = Depends(get_user_id),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    try:
        services.update_blog(blog_id, user_id, blog_data, uow)
    except ServicesException as e:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=str(e))


@blog_router.post("/")
async def create_blog(
    blog_data: BlogCreate,
    user_id: int = Depends(get_user_id),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    try:
        services.create_blog(user_id, blog_data, uow)
    except ServicesException as e:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=str(e))


@blog_router.post("/{blog_id}/comments")
async def add_comment(
    comment_data: CommentCreate,
    blog_id: int,
    user_id: int = Depends(get_user_id),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    try:
        services.add_comment(blog_id, user_id, comment_data, uow)
    except ServicesException as e:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=str(e))


@blog_router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    user_id: int = Depends(get_user_id),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    pass


@blog_router.get("/{blog_id}/comments")
async def get_blog_comments(blog_id: int, uow: AbstractUnitOfWork = Depends(get_uow)):
    pass


@blog_router.put("/comments/{comment_id}")
async def udate_comment(
    blod_id: int,
    comment_data: CommentUpdate,
    user_id: int = Depends(get_user_id),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    pass
