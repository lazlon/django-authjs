import contextlib
from collections.abc import Callable

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponse

from authjs.models import Session


class AuthenticationMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        token = request.COOKIES.get("authjs.session-token")

        if not hasattr(request, "user"):
            raise ImproperlyConfigured(  # noqa: TRY003
                "Authjs authentication middleware has to come after builtin auth"  # noqa: EM101
                "'django.contrib.auth.middleware.AuthenticationMiddleware'"
                "'authjs.middleware.AuthenticationMiddleware'",
            )

        if token is None:
            return self.get_response(request)

        with contextlib.suppress(Session.DoesNotExist):
            session = Session.objects.get(session_key=token)
            setattr(request, "user", session.user.user)  # noqa: B010
            return self.get_response(request)

        return self.get_response(request)
