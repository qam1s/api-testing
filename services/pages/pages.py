from typing import Any

import allure

from helpers.service_data import ServiceDataModel
from services.api_client import ApiClient
from services.pages.payloads import PagePayloads
from services.pages.models import PageModel, DeletedPageModel


class PagesService(ApiClient):
    @allure.step("Create page")
    def create_page(
        self, expected_code: int = 201, validate: bool = True, **kwargs: Any
    ) -> ServiceDataModel:
        payload = PagePayloads(**kwargs)
        return self.post(
            endpoint="/pages",
            payload=payload,
            expected_code=expected_code,
            validate=validate,
            model=PageModel
        )

    @allure.step("Get page")
    def get_page(
        self, pid: int, expected_code: int = 200, validate: bool = True
    ) -> ServiceDataModel:
        return self.get(
            endpoint=f"/pages/{pid}",
            expected_code=expected_code,
            validate=validate,
            model=PageModel
        )

    @allure.step("Update page")
    def update_page(
        self,
        pid: int,
        expected_code: int = 200,
        validate: bool = True,
        **kwargs: Any
    ) -> ServiceDataModel:
        payload = PagePayloads(**kwargs)
        return self.put(
            endpoint=f"/pages/{pid}",
            payload=payload,
            expected_code=expected_code,
            validate=validate,
            model=PageModel
        )

    @allure.step("Delete page")
    def delete_page(
        self, pid: int, expected_code: int = 200, validate: bool = True,
    ) -> ServiceDataModel:
        return self.delete(
            endpoint=f"/pages/{pid}",
            expected_code=expected_code,
            validate=validate,
            model=DeletedPageModel,
            params={"reassign": "", "force": "true"}
        )
