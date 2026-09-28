import allure
from pydantic import BaseModel, ValidationError


class Checkers:
    @staticmethod
    @allure.step("Check status code {expected_code}")
    def check_status_code(expected_code: int, actual_code: int) -> None:
        assert expected_code == actual_code, f"\n \
    Expected status code: {expected_code}\n \
    Actual status code: {actual_code}"

    @staticmethod
    def validate(model: type[BaseModel], data: dict) -> BaseModel:
        try:
            return model.model_validate(data)
        except ValidationError as e:
            raise AssertionError(e)
