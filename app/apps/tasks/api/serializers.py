from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.tasks.models import Task
from todo.utils.serializers import ReadOnlyModelSerializer, RecursiveSerializerField

if TYPE_CHECKING:
    from django.db.models import BaseManager


class UsersTaskField(serializers.SlugRelatedField):
    """Field that retrieves user tasks in `get_queryset`."""

    def __init__(self, source='parent', slug_field='uuid', **kwargs) -> None:
        super().__init__(source=source, slug_field=slug_field, **kwargs)

    def get_queryset(self) -> BaseManager[Task]:
        assert self.context.get('request', False)

        user = self.context['request'].user
        return Task.objects.filter(user=user)


class BaseTaskMeta:
    model = Task


# Task serializers
###############################################################################


class TaskNestedSerializer(ReadOnlyModelSerializer):
    """:class:`~Task` serializer used for listing.

    Uses :class:`~RecursiveSerializerField` for serializing all subtasks.
    """

    parent_uuid = serializers.SerializerMethodField()
    subtasks = RecursiveSerializerField(many=True)

    class Meta(BaseTaskMeta):
        fields = [
            'title',
            'completed',
            'uuid',
            'parent_uuid',
            'subtasks',
            'created',
        ]

    def get_parent_uuid(self, instance: Task) -> None | uuid.UUID:
        return None if instance.parent is None else instance.parent.uuid


class TaskListSerializer(TaskNestedSerializer):
    """:class:`~Task` serializer used for listing.

    Subtasks are displayed as :class:`~uuid.UUID`.
    """

    subtasks = serializers.SerializerMethodField()

    def get_subtasks(self, instance: Task) -> list[uuid.UUID]:
        return [subtask.uuid for subtask in instance.subtasks.all()]


class TaskCreateSerializer(serializers.ModelSerializer):
    """:class:`~Task` serializer used for creating."""

    parent_uuid = UsersTaskField(required=False, allow_null=True)

    class Meta(BaseTaskMeta):
        fields = [
            'title',
            'uuid',
            'parent_uuid',
            'completed',
        ]
        extra_kwargs = {'completed': {'read_only': True}}

    def create(self, validated_data: dict) -> Task:
        assert self.context.get('request', False)

        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_parent_uuid(self, value: Task | None) -> Task | None:
        if value is None:
            return value

        if isinstance(value.parent, Task):
            raise serializers.ValidationError(_("Cannot assign a subtask to a task which has a parent."))

        return value


class TaskUpdateSerializer(serializers.ModelSerializer):
    """:class:`~Task` serializer used for updating."""

    instance: Task

    parent_uuid = UsersTaskField(required=False, allow_null=True)

    class Meta(BaseTaskMeta):
        fields = [
            'title',
            'completed',
            'parent_uuid',
        ]

    def validate_parent_uuid(self, value: Task | None) -> Task | None:
        if value is None:
            return value

        if isinstance(value.parent, Task):
            raise serializers.ValidationError(_("Cannot assign a subtask to a task which has a parent."))

        if value.pk == self.instance.pk:
            raise serializers.ValidationError(_("Cannot assign subtask to itself."))

        if self.instance.subtasks.all():
            raise serializers.ValidationError(_("Cannot assign subtask. Task has subtasks."))

        return value
