"""
https://authjs.dev/reference/core/adapters#adapter
"""

import logging
from datetime import datetime

from django.contrib.auth import get_user_model

import authjs.models as m

logger = logging.getLogger(__name__)

from typing import Literal, TypedDict  # noqa: E402


class User(TypedDict):
    id: str | None
    name: str | None
    email: str | None
    emailVerified: datetime | None
    image: str | None


class Account(TypedDict):
    access_token: str | None
    token_type: str | None
    id_token: str | None
    refresh_token: str | None
    scope: str | None
    expires_at: int | None
    session_state: str | None

    providerAccountId: str
    userId: str
    provider: str
    type: Literal["oauth", "email", "credentials"]


class Session(TypedDict):
    expires: datetime
    sessionToken: str
    userId: str


class VerificationToken(TypedDict):
    identifier: str
    expires: datetime
    token: str


# User Management
def create_user(user: User) -> User:
    builtin, _ = get_user_model().objects.get_or_create(
        email=user.get("email"),
        username=user.get("name") or "",
    )

    out, created = m.User.objects.get_or_create(
        id=user.get("id"),
        defaults={
            "id": user.get("id"),
            "user": builtin,
            "name": user.get("name"),
            "email": user.get("email"),
            "email_verified": user.get("emailVerified"),
            "image": user.get("image"),
        },
    )
    if created:
        out.save()
    return User(
        id=out.id,
        name=out.name,
        email=out.email,
        emailVerified=out.email_verified,
        image=out.image,
    )


def get_user(user: dict) -> User:
    u = m.User.objects.get(pk=user["userId"])
    return User(
        id=u.id,
        name=u.name,
        email=u.email,
        emailVerified=u.email_verified,
        image=u.image,
    )


def get_user_by_account(acc: Account) -> User:
    account = m.Account.objects.get(
        provider_account_id=acc["providerAccountId"],
        provider=acc["provider"],
        user__id=acc["userId"],
    )
    return User(
        id=account.user.id,
        name=account.user.name,
        email=account.user.email,
        emailVerified=account.user.email_verified,
        image=account.user.image,
    )


def update_user(user: User) -> User:
    usr = m.User.objects.get(pk=user["id"])
    usr.name = user.get("name", usr.name)
    usr.email = user.get("email", usr.email)
    usr.email_verified = user.get("emailVerified", usr.email_verified)
    usr.image = user.get("image", usr.image)
    usr.save()
    return User(
        id=usr.id,
        name=usr.name,
        email=usr.email,
        emailVerified=usr.email_verified,
        image=usr.image,
    )


def link_account(account: Account) -> Account | dict:
    try:
        acc, _ = m.Account.objects.get_or_create(
            user=m.User.objects.get(pk=account["userId"]),
            provider=account.get("provider"),
            provider_account_id=account.get("providerAccountId"),
        )

        acc.access_token = account.get("access_token")
        acc.token_type = account.get("token_type")
        acc.id_token = account.get("id_token")
        acc.refresh_token = account.get("refresh_token")
        acc.scope = account.get("scope")
        acc.expires_at = account.get("expires_at")
        acc.session_state = account.get("session_state")
        acc.type = account.get("type")
        acc.save()

        return Account(
            access_token=acc.access_token,
            token_type=acc.token_type,
            id_token=acc.id_token,
            refresh_token=acc.refresh_token,
            scope=acc.scope,
            expires_at=acc.expires_at,
            session_state=acc.session_state,
            providerAccountId=acc.provider_account_id,
            provider=acc.provider,
            userId=acc.user.id,
            type=acc.type,
        )
    except Exception:
        logger.exception(f"Could not link account {account['userId']}")
        return {}


def delete_user(user: dict) -> User:
    u = m.User.objects.get(pk=user["userId"])
    usr = User(
        id=u.id,
        name=u.name,
        email=u.email,
        emailVerified=u.email_verified,
        image=u.image,
    )
    u.delete()
    return usr


def unlink_account(account: Account) -> Account:
    a = m.Account.objects.get(
        provider_account_id=account["providerAccountId"],
        provider=account["providerAccountId"],
        user__id=account["userId"],
    )
    acc = Account(
        access_token=a.access_token,
        token_type=a.token_type,
        id_token=a.id_token,
        refresh_token=a.refresh_token,
        scope=a.scope,
        expires_at=a.expires_at,
        session_state=a.session_state,
        providerAccountId=a.provider_account_id,
        provider=a.provider,
        userId=a.user.id,
        type=a.type,
    )
    a.delete()
    return acc


# Session Management
def create_session(session: Session) -> Session:
    s = m.Session(
        session_key=session["sessionToken"],
        user=m.User.objects.get(pk=session["userId"]),
        expires=session["expires"],
    )
    s.save()
    return Session(
        sessionToken=s.session_token,
        userId=s.user.id,
        expires=s.expires,
    )


def get_session_and_user(session: Session) -> dict:
    s = m.Session.objects.get(session_key=session["sessionToken"])
    return {
        "session": Session(
            sessionToken=s.session_token,
            userId=s.user.id,
            expires=s.expires,
        ),
        "user": User(
            id=s.user.id,
            name=s.user.name,
            email=s.user.email,
            emailVerified=s.user.email_verified,
            image=s.user.image,
        ),
    }


def update_session(session: Session) -> Session:
    s = m.Session.objects.get(session_key=session["sessionToken"])
    s.expires = session.get("expires", s.expires)
    if session["userId"] is not None:
        s.user = m.User.objects.get(pk=session["userId"])

    s.save()
    return Session(
        sessionToken=s.session_token,
        userId=s.user.id,
        expires=s.expires,
    )


def delete_session(session: Session) -> Session:
    s = m.Session.objects.get(session_key=session["sessionToken"])
    session = Session(
        sessionToken=s.session_token,
        userId=s.user.id,
        expires=s.expires,
    )
    s.delete()
    return session


# VerificationToken Management
def get_user_by_email(user: User) -> User:
    u = m.User.objects.get(email=user["email"])
    return User(
        id=u.id,
        name=u.name,
        email=u.email,
        emailVerified=u.email_verified,
        image=u.image,
    )


def create_verification_token(verification_token: VerificationToken) -> VerificationToken:
    m.VerificationToken(
        identifier=verification_token["identifier"],
        expires=verification_token["expires"],
        token=verification_token["token"],
    ).save()
    return verification_token


def use_verification_token(verification_token: VerificationToken) -> VerificationToken | dict:
    try:
        vtoken = m.VerificationToken.objects.get(
            token=verification_token["token"],
            identifier=verification_token["identifier"],
        )
        token = VerificationToken(
            token=vtoken.token,
            identifier=vtoken.identifier,
            expires=vtoken.expires,
        )
        vtoken.delete()
    except Exception:
        logger.exception(f"Could not use verification token: {verification_token['token']}")
        return {}
    else:
        return token
