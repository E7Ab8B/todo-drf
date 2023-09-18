from django.contrib.auth import forms as admin_forms
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    """Form for :class:`User` creation in the Admin Area."""

    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """Form for :class:`User` creation in the Admin Area."""

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        error_messages = {'username': {'unique': _("This username has already been taken.")}}
