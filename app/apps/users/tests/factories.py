from __future__ import annotations

from typing import TYPE_CHECKING, Any

from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from apps.users.models import User
from todo.utils.factories import BaseMetaFactory  # pylint: disable=unused-import

if TYPE_CHECKING:
    from collections.abc import Sequence


class UserFactory(DjangoModelFactory, metaclass=BaseMetaFactory[User]):
    username = Faker('user_name')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')

    @post_generation
    def password(obj, create: bool, extracted: Sequence[Any], **kwargs) -> None:  # pylint: disable=unused-argument
        password = extracted or Faker(
            'password',
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ).evaluate(None, None, extra={'locale': None})

        obj.set_password(password)

    class Meta:
        model = User
        django_get_or_create = ['username']
