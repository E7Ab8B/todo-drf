from django.urls import resolve, reverse

from rest_framework.test import APITestCase

from apps.users.tests.factories import UserFactory


class URLTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()

    def test_task_detail(self) -> None:
        assert (
            reverse('api:user-detail', kwargs={'username': self.user.username}) == f'/api/users/{self.user.username}/'
        )
        assert resolve(f'/api/users/{self.user.username}/').view_name == 'api:user-detail'

    def test_user_list(self) -> None:
        assert reverse('api:user-list') == '/api/users/'
        assert resolve('/api/users/').view_name == 'api:user-list'

    def test_user_me(self) -> None:
        assert reverse('api:user-me') == '/api/users/me/'
        assert resolve('/api/users/me/').view_name == 'api:user-me'
