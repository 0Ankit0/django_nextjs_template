from django.core.management.base import BaseCommand
from finances.services import subscriptions
from multitenancy.models import Tenant


class Command(BaseCommand):
    help = "Creates stripe customer and schedule subscription plan"

    def handle(self, *args, **options):
        tenants = Tenant.objects.filter(djstripe_customers__isnull=True)
        for tenant in tenants:
            subscriptions.initialize_tenant(tenant=tenant)
