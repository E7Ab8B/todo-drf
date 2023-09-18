from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.users.api.serializers import UserSerializer
from apps.users.models import User

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from rest_framework.request import Request


class UserViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = UserSerializer
    queryset: QuerySet[User] = User.objects.all()
    lookup_field = 'username'

    def get_queryset(self, *args, **kwargs) -> QuerySet[User]:
        user = self.request.user

        assert isinstance(user, User)

        if user.is_staff:
            return self.queryset

        return self.queryset.filter(pk=self.request.user.pk)

    @action(detail=False)
    def me(self, request: Request) -> Response:
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
