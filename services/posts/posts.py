from typing import Any

import allure

from helpers.service_data import ServiceDataModel
from services.api_client import ApiClient
from services.posts.payloads import PostPayloads
from services.posts.models import PostModel, DeletedPostModel


class PostsService(ApiClient):
    @allure.step("Create post")
    def create_post(
        self,
        expected_code: int = 201,
        validate: bool = True,
        **kwargs: Any
    ) -> ServiceDataModel:
        payload = PostPayloads(**kwargs)
        return self.post(
            endpoint="/posts",
            payload=payload,
            expected_code=expected_code,
            validate=validate,
            model=PostModel
        )

    @allure.step("Get post")
    def get_post(
        self, pid: int, expected_code: int = 200, validate: bool = True
    ) -> ServiceDataModel:
        return self.get(
            endpoint=f"/posts/{pid}",
            expected_code=expected_code,
            validate=validate,
            model=PostModel
        )

    @allure.step("Update post")
    def update_post(
        self,
        pid: int,
        expected_code: int = 200,
        validate: bool = True,
        **kwargs: Any
    ) -> ServiceDataModel:
        payload = PostPayloads(**kwargs)
        return self.put(
            endpoint=f"/posts/{pid}",
            payload=payload,
            expected_code=expected_code,
            validate=validate,
            model=PostModel
        )

    @allure.step("Delete post")
    def delete_post(
        self,
        pid: int,
        expected_code: int = 200,
        validate: bool = True
    ) -> ServiceDataModel:
        return self.delete(
            endpoint=f"/posts/{pid}",
            expected_code=expected_code,
            validate=validate,
            model=DeletedPostModel,
            params={"reassign": "", "force": "true"}
        )
