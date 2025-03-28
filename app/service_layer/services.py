from datetime import datetime

from app import utils
from app.domain.models.auth import User
from app.domain.models.blog import Blog, BlogStatus, Comment, Tag
from app.domain.schemas.auth import UserAuth, UserRegister
from app.domain.schemas.blog import (
    BlogBase,
    BlogCreate,
    BlogStatusChange,
    CommentCreate,
    CommentUpdate,
)
from app.service_layer.exceptions import (
    BlogDidNotExist,
    BlogDidNotPublish,
    IncorrectCommentId,
    IncorrectLoginOrPasswordException,
    IncorrectUserId,
    UserNotOwnerBlogException,
    UserNotOwnerCommentException,
    UserRegisteredException,
)
from app.service_layer.unit_of_work import AbstractUnitOfWork


def register_user(user_data: UserRegister, uow: AbstractUnitOfWork):
    with uow:
        user = uow.users.get_by_email(user_data.email)
        if user is not None:
            raise UserRegisteredException(user_data.email)

        user_data_dict = user_data.model_dump()
        del user_data_dict["confirm_password"]
        user = User(**user_data_dict)

        uow.users.add(user)
        uow.commit()


def auth_user(user_data: UserAuth, uow: AbstractUnitOfWork) -> int:
    with uow:
        user = uow.users.get_by_email(user_data.email)
        if user and utils.verify_password(user_data.password, user.password):
            return user.id
        else:
            raise IncorrectLoginOrPasswordException


def create_blog(user_id: int, blog_data: BlogCreate, uow: AbstractUnitOfWork):
    with uow:
        user = uow.users.get(user_id)

        if not user:
            raise IncorrectUserId

        tags = []
        for tag_data in blog_data.tags:
            tag = uow.tags.get_by_name(tag_data.name)
            if not tag:
                tag = Tag(**tag_data.model_dump())
                uow.tags.add(tag)
            tags.append(tag)

        blog_data_dict = blog_data.model_dump()
        blog_data_dict["tags"] = tags
        blog_data_dict["author_id"] = user.id

        blog = Blog(status=BlogStatus.HIDE, date_publish=None, **blog_data_dict)
        blog.author = user
        uow.blogs.add(blog)
        uow.commit()


def update_blog(blog_id: int, user_id: int, blog_data: BlogBase, uow: AbstractUnitOfWork):
    with uow:
        blog_to_update = uow.blogs.get(blog_id)
        user = uow.users.get(user_id)

        if not user:
            raise IncorrectUserId

        if user.id != blog_to_update.author_id:
            raise UserNotOwnerBlogException

        blog_to_update.title = blog_data.title
        blog_to_update.body = blog_data.body
        uow.commit()


def delete_blog(blog_id: int, user_id: int, uow: AbstractUnitOfWork):
    with uow:
        blog = uow.blogs.get(blog_id)
        user = uow.users.get(user_id)

        if not user:
            raise IncorrectUserId

        if not blog:
            return BlogDidNotExist

        if blog.author_id != user.id:
            raise UserNotOwnerBlogException

        uow.blogs.delete(blog)
        uow.commit()


def update_blog_status(
    blog_id: int, user_id: int, blog_data: BlogStatusChange, uow: AbstractUnitOfWork
):
    with uow:
        blog = uow.blogs.get(blog_id)
        user = uow.users.get(user_id)

        if not user:
            raise IncorrectUserId

        if not blog:
            raise BlogDidNotExist

        if user.id != blog.author_id:
            raise UserNotOwnerBlogException

        blog.status = blog_data.status
        if blog_data.status == BlogStatus.PUBLISH:
            blog.date_publish = datetime.now()

        uow.commit()


def add_comment(
    blog_id: int, user_id: int, comment_data: CommentCreate, uow: AbstractUnitOfWork
):
    with uow:
        blog = uow.blogs.get(blog_id)
        user = uow.users.get(user_id)

        if not user:
            raise IncorrectUserId

        if not blog:
            raise BlogDidNotExist

        if blog.status is not BlogStatus.PUBLISH:
            raise BlogDidNotPublish

        comment = Comment(
            date_publish=datetime.now(),
            author_id=user_id,
            blog_id=blog_id,
            **comment_data.model_dump(),
        )
        uow.comments.add(comment)
        uow.commit()


def delete_comment(user_id: int, comment_id: int, uow: AbstractUnitOfWork):
    with uow:
        comment = uow.comments.get(comment_id)
        user = uow.users.get(user_id)

        if not user:
            raise IncorrectUserId

        if not comment:
            raise IncorrectCommentId

        if user_id != comment.author_id:
            raise UserNotOwnerCommentException

        uow.comments.delete(comment)
        uow.commit()


def update_comment(
    user_id: int, comment_id: int, comment_data: CommentUpdate, uow: AbstractUnitOfWork
):
    with uow:
        comment = uow.comments.get(comment_id)
        user = uow.users.get(user_id)

        if not user:
            raise IncorrectUserId

        if not comment:
            raise IncorrectCommentId

        if user_id != comment.author_id:
            raise UserNotOwnerCommentException

        comment.text = comment_data.text
        uow.commit()


def get_blog_comments(blog_id: int, uow: AbstractUnitOfWork):
    with uow:
        return uow.comments.get_blog_comments(blog_id)
