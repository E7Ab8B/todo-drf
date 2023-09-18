from django.test import TestCase
from django.urls import reverse

from apps.users.tests.factories import UserFactory


class TestUserAdmin(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.superuser = UserFactory(is_superuser=True, is_staff=True)
        cls.user = UserFactory()

    def test_swagger_ui_accessible_by_superuser(self) -> None:
        url = reverse('api-docs')

        self.client.force_login(self.superuser)
        response = self.client.get(url)

        assert response.status_code == 200

    def test_swagger_ui_not_accessible_by_normal_user(self) -> None:
        url = reverse('api-docs')

        self.client.force_login(self.user)
        response = self.client.get(url)

        assert response.status_code == 403

    def test_api_schema_generated_successfully(self) -> None:
        url = reverse('api-schema')

        self.client.force_login(self.superuser)
        response = self.client.get(url)

        assert response.status_code == 200

    def test_api_schema_not_accessible_by_normal_user(self) -> None:
        url = reverse('api-schema')

        self.client.force_login(self.user)
        response = self.client.get(url)

        assert response.status_code == 403
