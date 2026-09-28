import allure

from helpers.db import DBConnector, UserRecord
from helpers.service_data import ServiceDataModel
from services.users.users import UsersService


@allure.epic("API")
@allure.feature("Users")
@allure.severity(allure.severity_level.BLOCKER)
class TestUsers:
    @allure.title("Create user")
    def test_create_user(
        self, db: DBConnector, delete_user: ServiceDataModel
    ):
        received_user = db.get_user_by_id(delete_user.model.id)
        assert (
            delete_user.payloads.username == received_user[0][0]
        ), f"Field 'username' values do not match, \
            {delete_user.payloads.username} != {received_user[0][0]}"
        assert (
            delete_user.payloads.email == received_user[0][1]
        ), f"Field 'email' values do not match, \
            {delete_user.payloads.email} != {received_user[0][1]}"

    @allure.title("Get user")
    def test_get_user(
        self, create_user_by_db: UserRecord, users_service: UsersService
    ):
        received_user = users_service.get_user(create_user_by_db.id)
        assert (
            create_user_by_db.username == received_user.model.name
        ), f"Field 'name' values do not match, \
            {create_user_by_db.username} != {received_user.model.name}"

    @allure.title("Update user")
    def test_update_user(
        self,
        db: DBConnector,
        users_service: UsersService,
        delete_user: ServiceDataModel
    ):
        updated_user = users_service.update_user(delete_user.model.id)
        received_user = db.get_user_by_id(delete_user.model.id)
        assert (
            updated_user.payloads.email == received_user[0][1]
        ), f"Field 'email' values do not match, \
            {updated_user.payloads.email} != {received_user[0][1]}"

    @allure.title("Delete user")
    def test_delete_user(
        self,
        db: DBConnector,
        users_service: UsersService,
        create_user: ServiceDataModel
    ):
        deleted_user = users_service.delete_user(create_user.model.id)
        received_user = db.get_user_by_id(create_user.model.id)
        assert (
            deleted_user.model.deleted is True and received_user == []
        ), f"User was not deleted, user = {received_user}"
