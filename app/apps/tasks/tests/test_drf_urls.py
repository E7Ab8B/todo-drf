from __future__ import annotations

from django.urls import resolve, reverse

from rest_framework.test import APITestCase

from apps.tasks.tests.factories import TaskFactory


class URLTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.task = TaskFactory()

    def test_task_detail(self) -> None:
        assert reverse('api:task-detail', kwargs={'uuid': self.task.uuid}) == f'/api/tasks/{self.task.uuid}/'
        assert resolve(f'/api/tasks/{self.task.uuid}/').view_name == 'api:task-detail'

    def test_task_list(self) -> None:
        assert reverse('api:task-list') == '/api/tasks/'
        assert resolve('/api/tasks/').view_name == 'api:task-list'

    def test_task_nested(self) -> None:
        assert reverse('api:task-nested') == '/api/tasks/nested/'
        assert resolve('/api/tasks/nested/').view_name == 'api:task-nested'

    def test_task_completed(self) -> None:
        assert reverse('api:task-completed') == '/api/tasks/completed/'
        assert resolve('/api/tasks/completed/').view_name == 'api:task-completed'

    def test_task_not_completed(self) -> None:
        assert reverse('api:task-not-completed') == '/api/tasks/not-completed/'
        assert resolve('/api/tasks/not-completed/').view_name == 'api:task-not-completed'

    def test_task_add_child(self) -> None:
        assert (
            reverse('api:task-add-child', kwargs={'uuid': self.task.uuid}) == f'/api/tasks/{self.task.uuid}/add-child/'
        )
        assert resolve(f'/api/tasks/{self.task.uuid}/add-child/').view_name == 'api:task-add-child'
