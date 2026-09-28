from typing import Generator

import pytest

from helpers.db import (
    CommentRecord,
    DBConnector,
    PageRecord,
    PostRecord,
    UserRecord,
)
from helpers.service_data import ServiceDataModel
from services.comments.comments import CommentsService
from services.pages.pages import PagesService
from services.posts.posts import PostsService
from services.users.users import UsersService


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[DBConnector, None, None]:
    db = DBConnector()
    yield db
    db.disconnect()


# comments

@pytest.fixture()
def comments_service() -> CommentsService:
    comments_service = CommentsService()
    return comments_service


@pytest.fixture()
def create_comment(
    comments_service: CommentsService, delete_post: ServiceDataModel
) -> ServiceDataModel:
    return comments_service.create_comment(delete_post.model.id)


@pytest.fixture()
def delete_comment(
    comments_service: CommentsService, create_comment: ServiceDataModel
) -> Generator[ServiceDataModel, None, None]:
    yield create_comment
    comments_service.delete_comment(create_comment.model.id)


@pytest.fixture()
def create_comment_by_db(
    db: DBConnector,
) -> Generator[CommentRecord, None, None]:
    comment = db.create_comment()
    yield comment
    db.delete_comment(comment.id)


# pages

@pytest.fixture()
def pages_service() -> PagesService:
    pages_service = PagesService()
    return pages_service


@pytest.fixture()
def create_page(pages_service: PagesService) -> ServiceDataModel:
    return pages_service.create_page()


@pytest.fixture()
def delete_page(
    pages_service: PagesService, create_page: ServiceDataModel
) -> Generator[ServiceDataModel, None, None]:
    yield create_page
    pages_service.delete_page(create_page.model.id)


@pytest.fixture()
def create_page_by_db(db: DBConnector) -> Generator[PageRecord, None, None]:
    page = db.create_page()
    yield page
    db.delete_page(page.id)


# posts

@pytest.fixture()
def posts_service() -> PostsService:
    posts_service = PostsService()
    return posts_service


@pytest.fixture()
def create_post(posts_service: PostsService) -> ServiceDataModel:
    return posts_service.create_post()


@pytest.fixture()
def delete_post(
    posts_service: PostsService, create_post: ServiceDataModel
) -> Generator[ServiceDataModel, None, None]:
    yield create_post
    posts_service.delete_post(create_post.model.id)


@pytest.fixture()
def create_post_by_db(db: DBConnector) -> Generator[PostRecord, None, None]:
    post = db.create_post()
    yield post
    db.delete_post(post.id)


# users

@pytest.fixture()
def users_service() -> UsersService:
    users_service = UsersService()
    return users_service


@pytest.fixture()
def create_user(users_service: UsersService) -> ServiceDataModel:
    return users_service.create_user()


@pytest.fixture()
def delete_user(
    users_service: UsersService, create_user: ServiceDataModel
) -> Generator[ServiceDataModel, None, None]:
    yield create_user
    users_service.delete_user(create_user.model.id)


@pytest.fixture()
def create_user_by_db(db: DBConnector) -> Generator[UserRecord, None, None]:
    user = db.create_user()
    yield user
    db.delete_user(user.id)
