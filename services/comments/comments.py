from typing import Any

import allure

from helpers.service_data import ServiceDataModel
from services.api_client import ApiClient
from services.comments.models import CommentModel, DeletedCommentModel
from services.comments.payloads import (
    CreateCommentPayloads, UpdateCommentPayloads
)


class CommentsService(ApiClient):
    @allure.step("Create comment")
    def create_comment(
        self,
        post: int,
        expected_code: int = 201,
        validate: bool = True,
        **kwargs: Any
    ) -> ServiceDataModel:
        payload = CreateCommentPayloads(post=post, **kwargs)
        return self.post(
            endpoint="/comments",
            payload=payload,
            expected_code=expected_code,
            validate=validate,
            model=CommentModel
        )

    @allure.step("Get comment")
    def get_comment(
        self, cid: int, expected_code: int = 200, validate: bool = True
    ) -> ServiceDataModel:
        return self.get(
            endpoint=f"/comments/{cid}",
            expected_code=expected_code,
            validate=validate,
            model=CommentModel
        )

    @allure.step("Update comment")
    def update_comment(
        self,
        cid: int,
        expected_code: int = 200,
        validate: bool = True,
        **kwargs: Any
    ) -> ServiceDataModel:
        payload = UpdateCommentPayloads(**kwargs)
        return self.put(
            endpoint=f"/comments/{cid}",
            payload=payload,
            expected_code=expected_code,
            validate=validate,
            model=CommentModel
        )

    @allure.step("Delete comment")
    def delete_comment(
        self,
        cid: int,
        expected_code: int = 200,
        validate: bool = True,
    ) -> ServiceDataModel:
        return self.delete(
            endpoint=f"/comments/{cid}",
            expected_code=expected_code,
            validate=validate,
            model=DeletedCommentModel,
            params={"reassign": "", "force": "true"}
        )
