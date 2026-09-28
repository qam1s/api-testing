import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import allure
import mysql.connector
from dotenv import load_dotenv

from services.users.payloads import CreateUserPayloads
from services.pages.payloads import PagePayloads
from services.posts.payloads import PostPayloads
from services.comments.payloads import CreateCommentPayloads

load_dotenv()


@dataclass(frozen=True)
class UserRecord:
    id: int
    username: str


@dataclass(frozen=True)
class PageRecord:
    id: int
    title: str


@dataclass(frozen=True)
class PostRecord:
    id: int
    title: str


@dataclass(frozen=True)
class CommentRecord:
    id: int
    content: str


class DBConnector:
    """Direct MySQL access for cross-checking API results.

    Rows are created without an explicit id so AUTO_INCREMENT assigns it;
    the id is read back with LAST_INSERT_ID() on the same connection,
    which stays correct under parallel execution (unlike MAX(id) + 1).
    Table names assume the default WordPress `wp_` prefix.
    """

    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            **json.loads(os.getenv("DB"))
        )
        assert self.connection.is_connected(), "Database connection is not established"

    def db_request(self, query: tuple[str, list | None]) -> list:
        cursor = self.connection.cursor()
        try:
            cursor.execute(*query)
            data = cursor.fetchall()
            self.connection.commit()
            return data
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    @allure.step("Create user")
    def create_user(self, **kwargs: Any) -> UserRecord:
        username = CreateUserPayloads(**kwargs).username
        now = datetime.now()
        self.db_request(
            (
                """INSERT INTO wp_users (user_login, display_name,
                    user_registered) VALUES (%s, %s, %s)""",
                [username, username, now],
            )
        )
        uid = self.db_request(("SELECT LAST_INSERT_ID()",))[0][0]
        return UserRecord(id=uid, username=username)

    @allure.step("Get user")
    def get_user_by_id(self, uid: int) -> list:
        return self.db_request(
            (
                """SELECT user_login, user_email FROM wp_users
                    WHERE id = %s""",
                [uid],
            )
        )

    @allure.step("Delete user")
    def delete_user(self, uid: int) -> None:
        self.db_request(
            ("""DELETE FROM wp_users WHERE id = %s""", [uid])
        )

    @allure.step("Create page")
    def create_page(self, **kwargs: Any) -> PageRecord:
        title = PagePayloads(**kwargs).title
        now = datetime.now()
        self.db_request(
            (
                """INSERT INTO wp_posts (post_title, post_excerpt, post_content,
                    post_date, post_date_gmt, post_modified, post_modified_gmt,
                    post_type, post_content_filtered, to_ping, pinged)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                [title, title, title, now, now, now, now, "page", "", "", ""],
            )
        )
        pid = self.db_request(("SELECT LAST_INSERT_ID()",))[0][0]
        return PageRecord(id=pid, title=title)

    @allure.step("Get page")
    def get_page_by_id(self, pid: int) -> list:
        return self.db_request(
            ("""SELECT post_title FROM wp_posts WHERE id = %s""", [pid])
        )

    @allure.step("Delete page")
    def delete_page(self, pid: int) -> None:
        self.db_request(
            ("""DELETE FROM wp_posts WHERE id = %s""", [pid])
        )

    @allure.step("Create post")
    def create_post(self, **kwargs: Any) -> PostRecord:
        title = PostPayloads(**kwargs).title
        now = datetime.now()
        self.db_request(
            (
                """INSERT INTO wp_posts (post_title, post_excerpt, post_content,
                    post_date, post_date_gmt, post_modified, post_modified_gmt,
                    post_content_filtered, to_ping, pinged)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                [title, title, title, now, now, now, now, "", "", ""],
            )
        )
        pid = self.db_request(("SELECT LAST_INSERT_ID()",))[0][0]
        return PostRecord(id=pid, title=title)

    @allure.step("Get post")
    def get_post_by_id(self, pid: int) -> list:
        return self.db_request(
            ("""SELECT post_title FROM wp_posts WHERE id = %s""", [pid])
        )

    @allure.step("Delete post")
    def delete_post(self, pid: int) -> None:
        self.db_request(
            ("""DELETE FROM wp_posts WHERE id = %s""", [pid])
        )

    @allure.step("Create comment")
    def create_comment(self, **kwargs: Any) -> CommentRecord:
        content = CreateCommentPayloads(**kwargs).content
        now = datetime.now()
        self.db_request(
            (
                """INSERT INTO wp_comments (comment_content, comment_author,
                    comment_date, comment_date_gmt)
                    VALUES (%s, %s, %s, %s)""",
                [content, "Firstname.LastName", now, now],
            )
        )
        cid = self.db_request(("SELECT LAST_INSERT_ID()",))[0][0]
        return CommentRecord(id=cid, content=content)

    @allure.step("Get comment")
    def get_comment_by_id(self, cid: int) -> list:
        return self.db_request(
            (
                """SELECT comment_content, comment_post_ID FROM wp_comments
                    WHERE comment_ID = %s""",
                [cid],
            )
        )

    @allure.step("Delete comment")
    def delete_comment(self, cid: int) -> None:
        self.db_request(
            ("""DELETE FROM wp_comments WHERE comment_id = %s""", [cid])
        )

    def disconnect(self) -> None:
        self.connection.close()
