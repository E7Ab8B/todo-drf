from __future__ import annotations

import json

from django.db import transaction

from apps.tasks.api.serializers import TaskListSerializer, TaskNestedSerializer
from apps.tasks.api.views import TaskViewSet
from apps.tasks.tests.factories import TaskFactory
from apps.users.tests.factories import UserFactory
from todo.utils.tests.testcases import APIViewSetTest


class TestTaskViewSet(APIViewSetTest):
    viewset = TaskViewSet

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()

        cls.task = TaskFactory(user=cls.user)
        cls.completed_task = TaskFactory(user=cls.user, completed=True)

        # Order by created field
        cls.user_tasks = (cls.completed_task, cls.task)

    def test_get_queryset(self) -> None:
        """`get_queryset` must return only tasks that the user owns."""
        user2 = UserFactory()
        task2 = TaskFactory(user=user2)

        view = self.create_view_get_queryset(action='list')

        assert task2 not in (queryset := view.get_queryset())
        assert len(self.user_tasks) == len(queryset)
        assert all(task in queryset for task in self.user_tasks)

    def test_retrieve(self) -> None:
        request = self.create_request()
        response = self.render_view(
            actions={'get': 'retrieve'},
            request=request,
            uuid=self.task.uuid,
        )

        assert response.status_code == 200
        assert response.data == TaskNestedSerializer(self.task).data

    @transaction.atomic
    def test_create(self) -> None:
        data = {
            "title": TaskFactory.title.evaluate(None, None, {'locale': None}),
            "parent_uuid": str(self.task.uuid),
        }

        request = self.create_request(method='post', data=json.dumps(data))
        response = self.render_view(actions={'post': 'create'}, request=request)

        assert response.status_code == 201

    @transaction.atomic
    def test_partial_update(self) -> None:
        data = {'completed': True}

        request = self.create_request(method='patch', data=json.dumps(data))
        response = self.render_view(
            actions={'patch': 'partial_update'},
            request=request,
            uuid=self.task.uuid,
        )

        assert response.status_code == 200
        assert response.data['completed'] is True

    @transaction.atomic
    def test_update(self) -> None:
        data = {
            'title': self.task.title,
            'completed': True,
            'parent_uuid': None,
        }

        request = self.create_request(method='put', data=json.dumps(data))
        response = self.render_view(
            actions={'put': 'update'},
            request=request,
            uuid=self.task.uuid,
        )

        assert response.status_code == 200
        assert response.data['completed'] is True

    def test_list(self) -> None:
        request = self.create_request()
        response = self.render_view(actions={'get': 'list'}, request=request)

        assert response.status_code == 200
        assert response.data['count'] == len(self.user_tasks)
        assert response.data['results'] == TaskListSerializer(self.user_tasks, many=True).data

    def test_nested(self) -> None:
        request = self.create_request()
        response = self.render_view(actions={'get': 'nested'}, request=request)

        assert response.status_code == 200
        assert response.data['count'] == len(self.user_tasks)
        assert response.data['results'] == TaskNestedSerializer(self.user_tasks, many=True).data

    def test_completed(self) -> None:
        request = self.create_request()
        response = self.render_view(actions={'get': 'completed'}, request=request)

        assert response.status_code == 200
        assert response.data['count'] == 1
        assert response.data['results'] == TaskNestedSerializer([self.completed_task], many=True).data

    def test_not_completed(self) -> None:
        request = self.create_request()
        response = self.render_view(actions={'get': 'not_completed'}, request=request)

        assert response.status_code == 200
        assert response.data['count'] == 1
        assert response.data['results'] == TaskNestedSerializer([self.task], many=True).data

    def test_add_child(self) -> None:
        data = {'title': TaskFactory.title.evaluate(None, None, {'locale': None})}

        request = self.create_request(method='post', data=json.dumps(data))
        response = self.render_view(actions={'post': 'add_child'}, request=request, uuid=self.task.uuid)

        assert response.status_code == 201
        assert response.data['parent_uuid'] == self.task.uuid
