import allure

from helpers.db import CommentRecord, DBConnector
from helpers.service_data import ServiceDataModel
from services.posts.posts import PostsService
from services.comments.comments import CommentsService


@allure.epic("API")
@allure.feature("Comments")
@allure.severity(allure.severity_level.BLOCKER)
class TestComments:
    @allure.title("Create comment")
    def test_create_comment(
        self,
        db: DBConnector,
        delete_post: ServiceDataModel,
        comments_service: CommentsService
    ):
        created_comment = comments_service.create_comment(
            delete_post.model.id
        )
        received_comment = db.get_comment_by_id(created_comment.model.id)
        assert (
            created_comment.payloads.content == received_comment[0][0]
        ), f"Field 'content' values do not match, \
            {created_comment.payloads.content} != {received_comment[0][0]}"
        comments_service.delete_comment(created_comment.model.id)

    @allure.title("Get comment")
    def test_get_comment(
        self,
        create_comment_by_db: CommentRecord,
        comments_service: CommentsService
    ):
        received_comment = comments_service.get_comment(
            create_comment_by_db.id
        )
        content = received_comment.model.content.rendered[3:-5]
        assert (
            create_comment_by_db.content == content
        ), f"Field 'content' values do not match, \
            {create_comment_by_db.content} != {content}"

    @allure.title("Update comment")
    def test_update_comment(
        self,
        db: DBConnector,
        comments_service: CommentsService,
        delete_comment: ServiceDataModel
    ):
        updated_comment = comments_service.update_comment(
            delete_comment.model.id
        )
        received_comment = db.get_comment_by_id(delete_comment.model.id)
        assert (
            updated_comment.payloads.content == received_comment[0][0]
        ), f"Field 'content' values do not match, \
            {updated_comment.payloads.content} != {received_comment[0][0]}"

    @allure.title("Delete comment")
    def test_delete_comment(
        self,
        db: DBConnector,
        comments_service: CommentsService,
        create_comment: ServiceDataModel
    ):
        deleted_comment = comments_service.delete_comment(
            create_comment.model.id
        )
        received_comment = db.get_comment_by_id(create_comment.model.id)
        assert (
            deleted_comment.model.deleted is True and received_comment == []
        ), f"Comment was not deleted, comment = {received_comment}"
