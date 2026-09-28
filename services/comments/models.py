from pydantic import BaseModel, RootModel, HttpUrl
from typing import List, Dict, Any, Optional


class ContentModel(BaseModel):
    rendered: str


class AuthorAvatarUrlsModel(RootModel):
    root: Dict[str, HttpUrl]


class LinkModel(BaseModel):
    href: HttpUrl
    targetHints: Optional[Dict[str, Any]]


class LinksModel(BaseModel):
    self: List[LinkModel]
    collection: List[LinkModel]
    author: List[LinkModel]
    up: List[LinkModel]


class CommentModel(BaseModel):
    id: int
    post: int
    parent: int
    author: int
    author_name: str
    author_url: HttpUrl | str
    date: str
    date_gmt: str
    content: ContentModel
    link: HttpUrl | str
    status: str
    type: str
    author_avatar_urls: AuthorAvatarUrlsModel
    meta: List[Any] | Dict[str, Any]
    _links: LinksModel


class DeletedCommentModel(BaseModel):
    deleted: bool
    previous: CommentModel
