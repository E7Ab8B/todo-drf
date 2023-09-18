from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory, APITestCase

from apps.tasks.api.serializers import (
    RecursiveSerializerField,
    TaskCreateSerializer,
    TaskUpdateSerializer,
)
from apps.tasks.models import Task
from apps.tasks.tests.factories import TaskFactory
from apps.users.tests.factories import UserFactory

if TYPE_CHECKING:
    from typing_extensions import Self

    from django.core.handlers.wsgi import WSGIRequest


class TestTaskCreateSerializer(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.task = TaskFactory(user=cls.user)

    def get_request(self) -> WSGIRequest:
        request = APIRequestFactory().get(path='/fake-url/')
        request.user = self.user
        return request

    def test_expect_request(self) -> None:
        """Raises an `AssertionError` when request is not passed in context."""
        data = {'title': 'Task Title', 'parent_uuid': str(self.task.uuid)}
        serializer = TaskCreateSerializer(data=data)

        with pytest.raises(AssertionError):
            serializer.is_valid(raise_exception=True)

    @transaction.atomic
    def test_create_with_valid_data(self) -> None:
        data = {'title': 'Task Title', 'parent_uuid': str(self.task.uuid)}

        serializer = TaskCreateSerializer(data=data, context={'request': self.get_request()})
        serializer.is_valid(raise_exception=True)

        assert isinstance(serializer.save(), Task)

    @transaction.atomic
    def test_validate_parent_uuid_none(self) -> None:
        """Accept `None` for `parent_uuid`."""
        data = {'title': 'Task Title', 'parent_uuid': None}

        serializer = TaskCreateSerializer(data=data, context={'request': self.get_request()})
        serializer.is_valid(raise_exception=True)

        assert isinstance(serializer.save(), Task)

    @transaction.atomic
    def test_raise_validation_error_for_parent_that_has_parent(self) -> None:
        """Raises `ValidationError` if provided parent is a subtask."""
        subtask = TaskFactory(user=self.user, parent=self.task)
        data = {'title': 'Task Title', 'parent_uuid': str(subtask.uuid)}

        serializer = TaskCreateSerializer(data=data, context={'request': self.get_request()})

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestRecursiveField(APITestCase):
    def setUp(self) -> None:
        class Instance:
            def __init__(self, char: str, children: list[Self] | None = None) -> None:
                self.char = char
                self.children = None if children is None else children

        class ExampleSerializer(serializers.Serializer):  # pylint: disable=abstract-method
            char = serializers.CharField()
            children = RecursiveSerializerField(many=True)

        self.Instance = Instance
        self.Serializer = ExampleSerializer

    def test_representation(self) -> None:
        child = self.Instance(char='cba')
        parent = self.Instance(char='abc', children=[child])

        assert self.Serializer(parent).data['children'] == [self.Serializer(child).data]


class TestTaskUpdateSerializer(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.task = TaskFactory(user=cls.user)

    def get_request(self) -> WSGIRequest:
        request = APIRequestFactory().get(path='/fake-url/')
        request.user = self.user
        return request

    def test_expect_request(self) -> None:
        """Raises an `AssertionError` when request is not passed in context."""
        data = {'title': 'Task Title', 'parent_uuid': str(self.task.uuid)}
        serializer = TaskUpdateSerializer(instance=self.task, data=data)

        with pytest.raises(AssertionError):
            serializer.is_valid(raise_exception=True)

    @transaction.atomic
    def test_update_with_valid_data(self) -> None:
        serializer = TaskUpdateSerializer(
            instance=self.task,
            data={'completed': True},
            context={'request': self.get_request()},
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        assert serializer.save().completed is True

    @transaction.atomic
    def test_update_with_valid_parent(self) -> None:
        """Update parent with valid `parent_uuid`."""
        parent = TaskFactory(user=self.user)
        serializer = TaskUpdateSerializer(
            instance=self.task,
            data={'parent_uuid': str(parent.uuid)},
            context={'request': self.get_request()},
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        assert serializer.save().parent == parent

    @transaction.atomic
    def test_update_parent_that_has_parent(self) -> None:
        """Raises `ValidationError` if provided parent is a subtask."""
        subtask = TaskFactory(user=self.user, parent=self.task)
        serializer = TaskUpdateSerializer(
            instance=self.task,
            data={'parent_uuid': str(subtask.uuid)},
            context={'request': self.get_request()},
            partial=True,
        )

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_update_parent_with_itself(self) -> None:
        """Raises `ValidationError` if provided parent is the task being updated."""
        serializer = TaskUpdateSerializer(
            instance=self.task,
            data={'parent_uuid': str(self.task.uuid)},
            context={'request': self.get_request()},
            partial=True,
        )

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    @transaction.atomic
    def test_update_parent_task_with_subtasks(self) -> None:
        """Raises `ValidationError` if parent is provided and task has subtasks."""
        # Create subtask for `task`
        TaskFactory(user=self.user, parent=self.task)
        task2 = TaskFactory(user=self.user)
        serializer = TaskUpdateSerializer(
            instance=self.task,
            data={'parent_uuid': str(task2.uuid)},
            context={'request': self.get_request()},
            partial=True,
        )

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
