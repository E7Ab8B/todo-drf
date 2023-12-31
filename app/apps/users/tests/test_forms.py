"""
Module for all Form Tests.
"""
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from apps.users.forms import UserAdminCreationForm
from apps.users.models import User
from apps.users.tests.factories import UserFactory


class TestUserAdminCreationForm(TestCase):
    """
    Test class for all tests related to the UserAdminCreationForm
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user: User = UserFactory(first_name='James', last_name='Smith ')

    def test_username_validation_error_msg(self):
        """
        Tests UserAdminCreation Form's unique validator functions correctly by testing:
            1) A new user with an existing username cannot be added.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """

        # The user already exists,
        # hence cannot be created.
        form = UserAdminCreationForm(
            {
                'username': self.user.username,
                'password1': self.user.password,
                'password2': self.user.password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert 'username' in form.errors
        assert form.errors['username'][0] == _("This username has already been taken.")
