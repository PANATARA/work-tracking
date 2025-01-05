from typing import Any
from collections.abc import Callable
import contextlib
from rest_framework.request import Request
from rest_framework.exceptions import APIException
from django.contrib.auth.middleware import get_user
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from django.utils.functional import SimpleLazyObject
from django.core.cache import cache

from core.celery_tasks import trace_last_user_request
from apps.users.models.users import User


class UserMiddleware:

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: Request) -> Any:
        if not request.user.is_authenticated:

            request.user = SimpleLazyObject(
                lambda: self.get_user(request) or get_user(request)
            )

        if request.user.is_authenticated:
            self.update_last_user_request(request)

        return self.get_response(request)

    def get_user(self, request: Request) -> User | None:
        json_auth = JWTTokenUserAuthentication()

        with contextlib.suppress(APIException, TypeError):
            return json_auth.authenticate(request)[0]

    def update_last_user_request(self, request: Request):
        user_id = request.user.id

        last_user_request = cache.get(user_id)
        if not last_user_request:
            trace_last_user_request.delay(request.user.id)
