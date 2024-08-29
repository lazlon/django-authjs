"""
Models required by Auth.js
https://authjs.dev/concepts/database-models
"""

from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.contrib.sessions import models as session
from django.db import models as m


def generate_id() -> object:
    return uuid4().hex


# reusable apps are recommended to reference builtin User through ForeignKey
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#reusable-apps-and-auth-user-model
class User(m.Model):
    user = m.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=m.CASCADE,
        related_name="authjs_user",
    )
    id = m.CharField(primary_key=True, max_length=255, default=generate_id)
    name = m.CharField(max_length=255, null=True)
    email = m.EmailField(unique=True, max_length=255, null=True)
    email_verified = m.DateTimeField(null=True)
    image = m.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.name or self.email or self.id


class Account(m.Model):
    id = m.CharField(primary_key=True, max_length=255, default=generate_id)
    user = m.ForeignKey(User, related_name="accounts", on_delete=m.CASCADE)
    type = m.CharField(
        max_length=255,
        choices=m.TextChoices(
            "AccountType",
            ["oauth", "email", "credentials"],
        ).choices,
    )
    provider = m.CharField(max_length=255)
    provider_account_id = m.CharField(max_length=255)
    refresh_token = m.TextField(null=True)
    access_token = m.TextField(null=True)
    expires_at = m.IntegerField(null=True)
    token_type = m.CharField(max_length=255, null=True)
    scope = m.CharField(max_length=255, null=True)
    id_token = m.TextField(null=True)
    session_state = m.CharField(max_length=255, null=True)

    class Meta:
        unique_together = ("provider", "provider_account_id")

    def __str__(self) -> str:
        return f"{self.user}@{self.provider}"


# TODO: better integration with builtin sessions
class Session(session.Session):
    session_user = m.ForeignKey(
        User,
        related_name="sessions",
        on_delete=m.DO_NOTHING,
        db_column="user",
    )

    @property
    def user(self) -> User:
        return self.session_user

    @user.setter
    def user(self, user: User) -> None:
        self.session_user = user

    @property
    def session_token(self) -> str:
        return super().session_key

    @session_token.setter
    def session_token(self, key: str) -> None:
        self.session_key = key

    @property
    def expires(self) -> datetime:
        return self.expire_date

    @expires.setter
    def expires(self, expires: datetime) -> None:
        self.expire_date = expires

    def __str__(self) -> str:
        return f"Session@{self.user}"


# TODO: periodically cleanup
# https://authjs.dev/concepts/database-models#verificationtoken
class VerificationToken(m.Model):
    identifier = m.CharField(max_length=255)
    token = m.CharField(unique=True, max_length=255)
    expires = m.DateTimeField()

    class Meta:
        unique_together = ("identifier", "token")

    def __str__(self) -> str:
        return f"VerificationToken@{self.identifier}"
