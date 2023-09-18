from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class Task(TimeStampedModel):
    """Model for ToDo tasks."""

    uuid = models.UUIDField(
        default=uuid.uuid4,
        db_index=True,
        editable=False,
    )
    title = models.CharField(
        verbose_name=_("title"),
        max_length=255,
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    completed = models.BooleanField(
        verbose_name=_("completed"),
        default=False,
    )
    parent = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        related_name='subtasks',
        verbose_name=_("parent"),
        null=True,
    )

    subtasks: RelatedManager[Task]

    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")
        get_latest_by = 'created'

    def __str__(self) -> str:
        """Returns :attr:`title`."""
        return self.title

    def __repr__(self) -> str:
        pk, title = self.pk, self.title
        return f'<{self.__class__.__name__} {pk=} {title=}>'
