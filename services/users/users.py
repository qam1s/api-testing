from typing import Any

import allure

from helpers.service_data import ServiceDataModel
from services.api_client import ApiClient
from services.users.payloads import CreateUserPayloads, UpdateUserPayloads
from services.users.models import UserModel, DeletedUserModel


class UsersService(ApiClient):
    @allure.step("Create user")
    def create_user(
        self,
        expected_code: int = 201,
        validate: bool = True,
        **kwargs: Any
    ) -> ServiceDataModel:
        payload = CreateUserPayloads(**kwargs)
        return self.post(
            endpoint="/users",
            payload=payload,
            expected_code=expected_code,
            validate=validate,
            model=UserModel
        )

    @allure.step("Get user")
    def get_user(
        self, uid: int, expected_code: int = 200, validate: bool = True
    ) -> ServiceDataModel:
        return self.get(
            endpoint=f"/users/{uid}",
            expected_code=expected_code,
            validate=validate,
            model=UserModel
        )

    @allure.step("Update user")
    def update_user(
        self,
        uid: int,
        expected_code: int = 200,
        validate: bool = True,
        **kwargs: Any
    ) -> ServiceDataModel:
        payload = UpdateUserPayloads(**kwargs)
        return self.put(
            endpoint=f"/users/{uid}",
            payload=payload,
            expected_code=expected_code,
            validate=validate,
            model=UserModel
        )

    @allure.step("Delete user")
    def delete_user(
        self,
        uid: int,
        expected_code: int = 200,
        validate: bool = True
    ) -> ServiceDataModel:
        return self.delete(
            endpoint=f"/users/{uid}",
            expected_code=expected_code,
            validate=validate,
            model=DeletedUserModel,
            params={"reassign": "", "force": "true"}
        )
