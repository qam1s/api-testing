import os
from dataclasses import asdict
from typing import Any

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from pydantic import BaseModel

from helpers.allure import Allure
from helpers.checkers import Checkers
from helpers.service_data import ServiceDataModel

load_dotenv()


class ApiClient:
    """Thin wrapper over requests for the WordPress REST API.

    The client is stateless: the payload is passed into each call and the
    result is returned to the caller, so one service instance can be shared
    safely. Authentication uses a WordPress Application Password, because
    the REST API rejects logins with the plain account password (401).
    """

    def __init__(self) -> None:
        self.base_url = os.getenv("BASE_URL")
        self.credentials = os.getenv("USERNAME"), os.getenv("PASSWORD")

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        payload: Any = None,
        expected_code: int,
        validate: bool,
        model: type[BaseModel],
        **kwargs: Any,
    ) -> ServiceDataModel:
        url = self.base_url + endpoint
        response = requests.request(
            method=method,
            url=url,
            auth=HTTPBasicAuth(*self.credentials),
            json=asdict(payload) if payload else None,
            **kwargs,
        )
        Allure.attach_response_body(response)
        Checkers.check_status_code(expected_code, response.status_code)
        if not validate:
            return ServiceDataModel(payloads=payload)
        return ServiceDataModel(
            model=Checkers.validate(model, response.json()),
            payloads=payload,
        )

    def get(self, **kwargs: Any) -> ServiceDataModel:
        return self.request("GET", **kwargs)

    def post(self, **kwargs: Any) -> ServiceDataModel:
        return self.request("POST", **kwargs)

    def put(self, **kwargs: Any) -> ServiceDataModel:
        return self.request("PUT", **kwargs)

    def delete(self, **kwargs: Any) -> ServiceDataModel:
        return self.request("DELETE", **kwargs)
