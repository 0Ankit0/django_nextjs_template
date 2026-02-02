from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from rest_framework import serializers

if TYPE_CHECKING:
    from users.models import User

UserModel = get_user_model()


def get_role_names(user: "User") -> list[str]:
    return [group.name for group in user.groups.all()]


def get_user_avatar_url(user: "User") -> str | None:
    field = serializers.FileField()
    if hasattr(user, "profile") and user.profile.avatar:
        return field.to_representation(user.profile.avatar.thumbnail)
    return None
