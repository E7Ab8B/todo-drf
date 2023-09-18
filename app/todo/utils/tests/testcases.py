from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from rest_framework.test import APIRequestFactory, APITestCase

if TYPE_CHECKING:
    from django.core.handlers.wsgi import WSGIRequest

    from rest_framework.decorators import ViewSetAction
    from rest_framework.response import Response
    from rest_framework.viewsets import GenericViewSet

    from apps.users.models import User

FAKE_URL = '/fake-url/'


class APIViewSetTest(APITestCase):
    user: User
    viewset: type[GenericViewSet]

    def create_request(
        self,
        method: Literal['get', 'post', 'put', 'patch', 'delete'] = 'get',
        path: str = FAKE_URL,
        data: Any | None = None,
    ) -> WSGIRequest:
        return getattr(APIRequestFactory(), method)(
            path=path,
            data=data,
            content_type='application/json',
        )

    def create_view_get_queryset(self, action: str) -> GenericViewSet:
        """Creates instance of `viewset` and does not render it.

        Used to test `get_queryset` method.
        """
        view = self.viewset()

        request = self.create_request()
        request.user = self.user

        view.request = request  # type: ignore [reportGeneralTypeIssues]
        view.action = action

        return view

    def render_view(
        self,
        actions: dict[str, str | ViewSetAction],
        request: WSGIRequest,
        **view_kwargs,
    ) -> Response:
        assert hasattr(self, 'viewset'), "Attribute `viewset` was not set."

        # BUG: pyright on github ci fails here, does not recognize `viewset` as GenericViewSet type
        view = self.viewset.as_view(actions=actions)  # type: ignore [reportGeneralTypeIssues]

        assert hasattr(self, 'user'), "Attribute `user` was no set."

        request.user = self.user
        return view(request, **view_kwargs).render()
