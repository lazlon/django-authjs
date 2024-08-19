import json
import uuid
from datetime import timedelta
from typing import TypedDict
from urllib.parse import urlencode

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from authjs import adapter


def url(path: str, params: dict) -> str:
    return f"{reverse(path)}?{urlencode({
        key: value for key, value in params.items() if value is not None
    })}"


class User(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def create_user(self, user: adapter.User) -> None:
        response = self.client.post(url("create-user", {**user}))
        self.assertEqual(response.status_code, 200)

        res: adapter.User = json.loads(response.content)
        self.assertEqual(res["id"], user["id"])
        self.assertEqual(res["email"], user["email"])

    def get_user(self, user: adapter.User) -> None:
        response = self.client.get(url("get-user", {"userId":user["id"]}))
        self.assertEqual(response.status_code, 200)

        res: adapter.User = json.loads(response.content)
        self.assertEqual(res["id"], user["id"])
        self.assertEqual(res["email"], user["email"])
        self.assertEqual(res["image"], user["image"])

    def get_user_by_email(self, user: adapter.User) -> None:
        response = self.client.get(url("get-user-by-email", {**user}))
        self.assertEqual(response.status_code, 200)

        res: adapter.User = json.loads(response.content)
        self.assertDictEqual(res, user)

    def link_account(self, account: adapter.Account) -> None:
        response = self.client.post(url("link-account", {**account}))
        self.assertEqual(response.status_code, 200)

        res: adapter.Account = json.loads(response.content)
        self.assertEqual(res["access_token"], account["access_token"])
        self.assertEqual(res["userId"], account["userId"])

    def update_user(self, user: adapter.User) -> None:
        response = self.client.put(url("update-user", {**user}))
        self.assertEqual(response.status_code, 200)

    def get_user_by_account(self, user: adapter.User, account: adapter.Account) -> None:
        response = self.client.get(url("get-user-by-account", {**account}))
        self.assertEqual(response.status_code, 200)

        res: adapter.User = json.loads(response.content)
        self.assertEqual(res["id"], user["id"])
        self.assertEqual(res["email"], user["email"])
        self.assertEqual(res["image"], user["image"])

    def delete_user(self, user: adapter.User) -> None:
        response = self.client.delete(url("delete-user", {"userId":user["id"]}))
        self.assertEqual(response.status_code, 200)

    def test_user_methods(self) -> None:
        user = adapter.User(
            id="userid",
            email="john@doe.com",
            name="John Doe",
            emailVerified=None,
            image=None,
        )

        account = adapter.Account(
            access_token=uuid.uuid1().hex,
            token_type="",
            id_token="",
            refresh_token="",
            scope="",
            expires_at=0,
            session_state="",
            providerAccountId="test-id",
            userId=user.get("id") or "",
            provider="test",
            type="oauth",
        )

        self.create_user(user)
        self.get_user(user)
        self.get_user_by_email(user)

        user["image"] = "lorempicsum"
        self.update_user(user)
        self.get_user(user)

        self.link_account(account)
        self.get_user_by_account(user, account)
        self.delete_user(user)


class Session(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def create_session(self, session: adapter.Session) -> None:
        response = self.client.post(url("create-session", {**session}))
        self.assertEqual(response.status_code, 200)

        res: adapter.Session = json.loads(response.content)
        self.assertEqual(res["sessionToken"], session["sessionToken"])

    def get_session_and_user(self, session: adapter.Session, user: adapter.User) -> None:
        response = self.client.get(url("get-session-and-user", {**session}))
        self.assertEqual(response.status_code, 200)

        class SessionAndUser(TypedDict):
            session: adapter.Session
            user: adapter.User

        res: SessionAndUser = json.loads(response.content)
        self.assertEqual(res["user"]["id"], user["id"])
        self.assertEqual(session["sessionToken"], res["session"]["sessionToken"])

    def update_session(self, session: adapter.Session) -> None:
        response = self.client.put(url("update-session", {**session}))
        self.assertEqual(response.status_code, 200)

        res: adapter.Session = json.loads(response.content)
        self.assertEqual(session["sessionToken"], res["sessionToken"])

    def delete_session(self, session: adapter.Session) -> None:
        response = self.client.delete(url("delete-session", {**session}))
        self.assertEqual(response.status_code, 200)


    def test_in_session(self) -> None:
        user = adapter.User(
            id="userid",
            email="john@doe.com",
            name="John Doe",
            emailVerified=None,
            image=None,
        )

        session = adapter.Session(
            expires=timezone.now(),
            userId="userid",
            sessionToken=uuid.uuid1().hex,
        )

        adapter.create_user(user)
        self.create_session(session)
        self.get_session_and_user(session, user)

        session["expires"] += timedelta(days=1)
        self.update_session(session)
        self.get_session_and_user(session, user)

        self.delete_session(session)


class Verification(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def create_verification(self, token: adapter.VerificationToken) -> None:
        response = self.client.post(url("create-verification-token", {**token}))
        self.assertEqual(response.status_code, 200)

        res: adapter.VerificationToken = json.loads(response.content)
        self.assertEqual(res["token"], token["token"])
        self.assertEqual(res["identifier"], token["identifier"])

    def use_verification(self, token: adapter.VerificationToken) -> None:
        response = self.client.delete(url("use-verification-token", {**token}))
        self.assertEqual(response.status_code, 200)

        res: adapter.VerificationToken = json.loads(response.content)
        self.assertEqual(res["token"], token["token"])
        self.assertEqual(res["identifier"], token["identifier"])

    def test_verification_token(self) -> None:
        token = adapter.VerificationToken(
            identifier=uuid.uuid1().hex,
            expires=timezone.now(),
            token=uuid.uuid1().hex,
        )

        self.create_verification(token)
        self.use_verification(token)
