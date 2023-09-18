from django.db import transaction
from django.test import TestCase
from django.urls import reverse

from apps.users.models import User
from apps.users.tests.factories import UserFactory


class TestUserAdmin(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.superuser = UserFactory(is_superuser=True, is_staff=True)

    def test_changelist(self) -> None:
        url = reverse('admin:users_user_changelist')
        self.client.force_login(self.superuser)

        response = self.client.get(url)

        assert response.status_code == 200

    def test_search(self) -> None:
        url = reverse('admin:users_user_changelist')
        self.client.force_login(self.superuser)

        response = self.client.get(url, data={'q': 'test'})

        assert response.status_code == 200

    @transaction.atomic
    def test_add(self) -> None:
        url = reverse('admin:users_user_add')
        self.client.force_login(self.superuser)

        response = self.client.get(url)

        assert response.status_code == 200

    @transaction.atomic
    def test_add_user(self) -> None:
        """Successfully create a user."""
        password = 'R@ndom-P@ssw0rd'
        url = reverse('admin:users_user_add')
        self.client.force_login(self.superuser)

        response = self.client.post(url, data={'username': 'test', 'password1': password, 'password2': password})

        assert response.status_code == 302
        assert User.objects.filter(username='test').exists()

    def test_view_user(self) -> None:
        url = reverse('admin:users_user_change', kwargs={'object_id': self.superuser.pk})
        self.client.force_login(self.superuser)

        response = self.client.get(url)

        assert response.status_code == 200
