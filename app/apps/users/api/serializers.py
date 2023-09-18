from rest_framework import serializers

from apps.users.models import User
from todo.utils.serializers import ReadOnlyModelSerializer


class UserSerializer(ReadOnlyModelSerializer):
    """Main serializer that is used for :class:`~User`."""

    joined = serializers.ReadOnlyField(source='date_joined')

    class Meta:
        model = User
        fields = [
            'username',
            'url',
            'joined',
        ]

        extra_kwargs = {
            'url': {
                'view_name': 'api:user-detail',
                'lookup_field': 'username',
            },
        }
