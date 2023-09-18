from __future__ import annotations

from django.db import transaction

from apps.users.api.serializers import UserSerializer
from apps.users.api.views import UserViewSet
from apps.users.tests.factories import UserFactory
from todo.utils.tests.testcases import APIViewSetTest


class TestUserViewSet(APIViewSetTest):
    viewset = UserViewSet

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()

    def test_get_queryset(self) -> None:
        """`get_queryset` must return only the authenticated user."""
        view = self.create_view_get_queryset(action='list')

        assert self.user in (queryset := view.get_queryset())
        assert 1 == len(queryset)

    @transaction.atomic
    def test_get_queryset_staff(self) -> None:
        """`get_queryset` returns all users for staff."""
        view = self.create_view_get_queryset(action='list')
        view.request.user = UserFactory(is_staff=True)

        assert self.user in (queryset := view.get_queryset())
        assert 2 == len(queryset)

    def test_retrieve(self) -> None:
        request = self.create_request()
        response = self.render_view(
            actions={'get': 'retrieve'},
            request=request,
            username=self.user.username,
        )
        serializer_data = UserSerializer(self.user, context={'request': request}).data

        assert response.status_code == 200
        assert response.data == serializer_data

    def test_list(self) -> None:
        request = self.create_request()
        response = self.render_view(actions={'get': 'list'}, request=request)
        serializer_data = UserSerializer([self.user], many=True, context={'request': request}).data

        assert response.status_code == 200
        assert response.data['count'] == 1
        assert response.data['results'] == serializer_data

    def test_me(self) -> None:
        request = self.create_request()
        response = self.render_view(actions={'get': 'me'}, request=request)
        serializer_data = UserSerializer(self.user, context={'request': request}).data

        assert response.data == serializer_data
