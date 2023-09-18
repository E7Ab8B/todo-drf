from __future__ import annotations

from django.test import TestCase

from apps.tasks.tests.factories import TaskFactory


class TestTask(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.task = TaskFactory()

    def test_str(self) -> None:
        assert self.task.title == str(self.task)
