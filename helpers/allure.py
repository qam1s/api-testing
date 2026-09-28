import allure
from allure_commons.types import AttachmentType
from requests import Response


class Allure:
    @staticmethod
    def attach_response_body(response: Response) -> None:
        allure.attach(
            response.content,
            "Response body",
            AttachmentType.JSON
        )
