from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import serializers

if TYPE_CHECKING:
    from rest_framework.fields import Field


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    """Serializer that marks all fields as read only."""

    def get_fields(self, *args, **kwargs) -> dict[str, Field]:
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields


class RecursiveSerializerField(serializers.Serializer):  # pylint: disable=abstract-method
    """Recursive serializer used for nested self-referential objects.

    Must be called with argument ``many`` that is set to :obj:`True`.
    """

    def to_representation(self, instance) -> dict:
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data
