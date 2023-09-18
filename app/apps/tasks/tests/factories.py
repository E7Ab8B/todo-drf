from __future__ import annotations

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from apps.tasks.models import Task
from apps.users.tests.factories import UserFactory
from todo.utils.factories import BaseMetaFactory  # pylint: disable=unused-import


class TaskFactory(DjangoModelFactory, metaclass=BaseMetaFactory[Task]):
    # Returns a full-fledged `uuid.UUID` with cast_to set to `None`
    uuid = Faker('uuid4', cast_to=None)
    title = Faker('word')

    user = SubFactory(UserFactory)

    class Meta:
        model = Task
        django_get_or_create = ['uuid']
