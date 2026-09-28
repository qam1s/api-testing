import allure

from helpers.db import DBConnector, PageRecord
from helpers.service_data import ServiceDataModel
from services.pages.pages import PagesService


@allure.epic("API")
@allure.feature("Pages")
@allure.severity(allure.severity_level.BLOCKER)
class TestPages:
    @allure.title("Create page")
    def test_create_page(
        self, db: DBConnector, delete_page: ServiceDataModel
    ):
        received_page = db.get_page_by_id(delete_page.model.id)
        assert (
            delete_page.payloads.title == received_page[0][0]
        ), f"Field 'title' values do not match, \
            {delete_page.payloads.title} != {received_page[0][0]}"

    @allure.title("Get page")
    def test_get_page(
        self,
        create_page_by_db: PageRecord,
        pages_service: PagesService
    ):
        received_page = pages_service.get_page(
            create_page_by_db.id
        )
        assert (
            create_page_by_db.title == received_page.model.title.rendered
        ), f"Field 'title' values do not match, \
            {create_page_by_db.title} != {received_page.model.title.rendered}"

    @allure.title("Update page")
    def test_update_page(
        self,
        db: DBConnector,
        pages_service: PagesService,
        delete_page: ServiceDataModel
    ):
        updated_page = pages_service.update_page(delete_page.model.id)
        received_page = db.get_page_by_id(delete_page.model.id)
        assert (
            updated_page.payloads.title == received_page[0][0]
        ), f"Field 'title' values do not match, \
            {updated_page.payloads.title} != {received_page[0][0]}"

    @allure.title("Delete page")
    def test_delete_page(
        self,
        db: DBConnector,
        pages_service: PagesService,
        create_page: ServiceDataModel
    ):
        deleted_page = pages_service.delete_page(create_page.model.id)
        received_page = db.get_page_by_id(create_page.model.id)
        assert (
            deleted_page.model.deleted is True and received_page == []
        ), f"Page was not deleted, page = {received_page}"
