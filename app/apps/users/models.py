from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.postgres.fields import CICharField, CIEmailField
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """Model for ToDo users."""

    username_validator = ASCIIUsernameValidator()

    username = CICharField(
        verbose_name=_("username"),
        max_length=30,
        unique=True,
        help_text=_("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=150,
        blank=True,
    )
    email = CIEmailField(
        verbose_name=_("email address"),
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(
        verbose_name=_("date joined"),
        default=timezone.now,
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        get_latest_by = 'date_joined'

    def __str__(self) -> str:
        """Returns :attr:`full_name`."""
        return self.full_name

    def __repr__(self) -> str:
        pk, username = self.pk, self.username
        return f'<{self.__class__.__name__} {pk=} {username=}>'

    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    @admin.display(description=_("Full name"))
    def full_name(self) -> str:
        """Return the :attr:`first_name` plus the :attr:`last_name`.

        Adds a space in between them and strips from any leading or trailing
        spaces.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def email_user(
        self,
        subject: str,
        message: str,
        from_email: str | None = None,
        **kwargs,
    ) -> None:
        """Send an email to user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
