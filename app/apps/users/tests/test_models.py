from __future__ import annotations

import faker
import pytest

from django.core import mail
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.users.tests.factories import UserFactory


class UserTask(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory(
            username='USERname',
            first_name='James',
            last_name='Smith ',
        )

    def test_str(self) -> None:
        assert self.user.full_name == str(self.user)

    def test_full_name(self) -> None:
        assert self.user.full_name == 'James Smith'

    def test_clean(self) -> None:
        user = UserFactory.build(email='email@MAIL.com')

        user.clean()

        assert user.email == 'email@mail.com'

    def test_email_user(self) -> None:
        fake = faker.Faker()
        subject = fake.word()
        message = fake.sentence()

        self.user.email_user(subject, message)

        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == subject
        assert mail.outbox[0].body == message

    def test_case_insensitive_username(self) -> None:
        """`username` field should be case insensitive and raise and exception."""
        user2 = UserFactory.build(username='USERname')

        with pytest.raises(IntegrityError):
            user2.save()
