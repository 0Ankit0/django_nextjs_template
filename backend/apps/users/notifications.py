import logging

from core import emails

from . import email_serializers

logger = logging.getLogger(__name__)


class UserEmail(emails.Email):
    def __init__(self, user, data=None):
        super().__init__(to=user.email, data=data)


class AccountActivationEmail(UserEmail):
    name = "ACCOUNT_ACTIVATION"  # type: ignore[assignment]
    serializer_class = email_serializers.AccountActivationEmailSerializer  # type: ignore[assignment]


class PasswordResetEmail(UserEmail):
    name = "PASSWORD_RESET"  # type: ignore[assignment]
    serializer_class = email_serializers.PasswordResetEmailSerializer  # type: ignore[assignment]
