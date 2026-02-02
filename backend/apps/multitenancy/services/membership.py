from typing import TYPE_CHECKING, Optional

from django.contrib.auth import get_user_model

from ..constants import TenantUserRole
from ..models import Tenant, TenantMembership
from ..notifications import TenantInvitationEmail, send_tenant_invitation_notification
from ..tokens import tenant_invitation_token

if TYPE_CHECKING:
    from users.models import User

UserModel = get_user_model()


def create_tenant_membership(
    tenant: Tenant,
    user: Optional["User"] = None,
    creator: Optional["User"] = None,
    invitee_email_address: str = "",
    role: TenantUserRole = TenantUserRole.MEMBER,
    is_accepted: bool = False,
):
    membership = TenantMembership.objects.create(
        user=user,
        tenant=tenant,
        role=role,
        invitee_email_address=invitee_email_address,
        is_accepted=is_accepted,
        creator=creator,
    )
    if not is_accepted:
        # Use simple conditional assignment for email to avoid type errors
        email_to_use = invitee_email_address
        if not email_to_use and user:
            email_to_use = user.email

        token = tenant_invitation_token.make_token(user_email=email_to_use, tenant_membership=membership)
        # Use the membership ID directly instead of GraphQL global ID
        tenant_membership_id = str(membership.id)

        recipient_email = invitee_email_address
        if user:
            recipient_email = user.email

        TenantInvitationEmail(
            to=recipient_email,
            data={"tenant_membership_id": tenant_membership_id, "token": token},
        ).send()

        if user:
            send_tenant_invitation_notification(membership, tenant_membership_id, token)

    return membership
