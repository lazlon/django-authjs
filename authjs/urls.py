from collections.abc import Callable
from typing import Literal

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from authjs import adapter


def as_view(method: Literal["GET", "POST", "PUT", "DELETE"], fn: Callable) -> Callable:
    @csrf_exempt
    @require_http_methods([method])
    def view(request: HttpRequest) -> JsonResponse:
        try:
            return JsonResponse(fn(request.GET))
        except Exception as e:  # noqa: BLE001
            return JsonResponse({"errors": [str(e)]}, status=404)

    return view


urlpatterns = [
    path(
        "create-user/",
        as_view("POST", adapter.create_user),
        name="create-user",
    ),
    path(
        "get-user/",
        as_view("GET", adapter.get_user),
        name="get-user",
    ),
    path(
        "get-user-by-account/",
        as_view("GET", adapter.get_user_by_account),
        name="get-user-by-account",
    ),
    path(
        "update-user/",
        as_view("PUT", adapter.update_user),
        name="update-user",
    ),
    path(
        "link-account/",
        as_view("POST", adapter.link_account),
        name="link-account",
    ),
    path(
        "delete-user/",
        as_view("DELETE", adapter.delete_user),
        name="delete-user",
    ),
    path(
        "unlink-account/",
        as_view("DELETE", adapter.unlink_account),
        name="unlink-account",
    ),
    path(
        "create-session/",
        as_view("POST", adapter.create_session),
        name="create-session",
    ),
    path(
        "get-session-and-user/",
        as_view("GET", adapter.get_session_and_user),
        name="get-session-and-user",
    ),
    path(
        "update-session/",
        as_view("PUT", adapter.update_session),
        name="update-session",
    ),
    path(
        "delete-session/",
        as_view("DELETE", adapter.delete_session),
        name="delete-session",
    ),
    path(
        "get-user-by-email/",
        as_view("GET", adapter.get_user_by_email),
        name="get-user-by-email",
    ),
    path(
        "create-verification-token/",
        as_view("POST", adapter.create_verification_token),
        name="create-verification-token",
    ),
    path(
        "use-verification-token/",
        as_view("DELETE", adapter.use_verification_token),
        name="use-verification-token",
    ),
]
