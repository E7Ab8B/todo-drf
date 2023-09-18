from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.tasks.api.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskNestedSerializer,
    TaskUpdateSerializer,
)
from apps.tasks.models import Task

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from rest_framework.request import Request
    from rest_framework.serializers import Serializer


class TaskViewSet(ModelViewSet):
    serializer_action_classes = {
        'create': TaskCreateSerializer,
        'retrieve': TaskNestedSerializer,
        'update': TaskUpdateSerializer,
        'partial_update': TaskUpdateSerializer,
        'list': TaskListSerializer,
        # Custom actions
        'nested': TaskNestedSerializer,
        'completed': TaskNestedSerializer,
        'not_completed': TaskNestedSerializer,
        'add_child': TaskCreateSerializer,
    }
    queryset: QuerySet[Task] = Task.objects.all()
    lookup_field = 'uuid'

    def get_serializer_class(self) -> type[Serializer]:
        return self.serializer_action_classes[self.action]

    def get_queryset(self) -> QuerySet[Task]:
        queryset = (
            self.queryset.filter(user=self.request.user)
            .order_by('-completed')
            .select_related('parent')
            .prefetch_related('subtasks')
        )

        if self.action == 'completed':
            return queryset.filter(completed=True)
        if self.action == 'not_completed':
            return queryset.filter(completed=False)

        return queryset

    @action(detail=False)
    def nested(self, request: Request) -> Response:
        return super().list(request)

    @action(detail=False)
    def completed(self, request: Request) -> Response:
        return super().list(request)

    @action(detail=False, url_path='not-completed')
    def not_completed(self, request: Request) -> Response:
        return super().list(request)

    @action(methods=['post'], detail=True, url_path='add-child')
    def add_child(self, request: Request, uuid: str) -> Response:
        serializer = self.get_serializer_class()(
            data=request.data | {'parent_uuid': uuid},
            context=self.get_serializer_context(),
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
