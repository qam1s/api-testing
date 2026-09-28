import allure

from helpers.db import DBConnector, PostRecord
from helpers.service_data import ServiceDataModel
from services.posts.posts import PostsService


@allure.epic("API")
@allure.feature("Posts")
@allure.severity(allure.severity_level.BLOCKER)
class TestPosts:
    @allure.title("Create post")
    def test_create_post(
        self, db: DBConnector, delete_post: ServiceDataModel
    ):
        received_post = db.get_post_by_id(delete_post.model.id)
        assert (
            delete_post.payloads.title == received_post[0][0]
        ), f"Field 'title' values do not match, \
            {delete_post.payloads.title} != {received_post[0][0]}"

    @allure.title("Get post")
    def test_get_post(
        self,
        create_post_by_db: PostRecord,
        posts_service: PostsService
    ):
        received_post = posts_service.get_post(
            create_post_by_db.id
        )
        assert (
            create_post_by_db.title == received_post.model.title.rendered
        ), f"Field 'title' values do not match, \
            {create_post_by_db.title} != {received_post.model.title.rendered}"

    @allure.title("Update post")
    def test_update_post(
        self,
        db: DBConnector,
        posts_service: PostsService,
        delete_post: ServiceDataModel
    ):
        updated_post = posts_service.update_post(delete_post.model.id)
        received_post = db.get_post_by_id(delete_post.model.id)
        assert (
            updated_post.payloads.title == received_post[0][0]
        ), f"Field 'title' values do not match, \
            {updated_post.payloads.title} != {received_post[0][0]}"

    @allure.title("Delete post")
    def test_delete_post(
        self,
        db: DBConnector,
        posts_service: PostsService,
        create_post: ServiceDataModel
    ):
        deleted_post = posts_service.delete_post(create_post.model.id)
        received_post = db.get_post_by_id(create_post.model.id)
        assert (
            deleted_post.model.deleted is True and received_post == []
        ), f"Post was not deleted, post = {received_post}"
