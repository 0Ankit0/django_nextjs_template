from unittest.mock import Mock

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from ..middleware import TenantMiddleware, get_current_tenant, get_current_user_role

pytestmark = pytest.mark.django_db


class TestGetCurrentTenant:
    def test_get_current_tenant_with_valid_id(self, tenant):
        result = get_current_tenant(tenant.id)
        assert result == tenant
        assert result.id == tenant.id

    def test_get_current_tenant_with_invalid_id(self):
        result = get_current_tenant("invalid-id")
        assert result is None

    def test_get_current_tenant_with_none(self):
        result = get_current_tenant(None)
        assert result is None


class TestGetCurrentUserRole:
    def test_get_current_user_role_with_valid_membership(self, user, tenant, tenant_membership):
        result = get_current_user_role(tenant, user)
        assert result == tenant_membership.role

    def test_get_current_user_role_without_membership(self, user, tenant):
        result = get_current_user_role(tenant, user)
        assert result is None

    def test_get_current_user_role_with_anonymous_user(self, tenant):
        anonymous_user = AnonymousUser()
        result = get_current_user_role(tenant, anonymous_user)
        assert result is None

    def test_get_current_user_role_with_none_tenant(self, user):
        result = get_current_user_role(None, user)
        assert result is None


class TestTenantMiddleware:
    def test_middleware_with_header(self, tenant, user):
        factory = RequestFactory()
        request = factory.get("/api/test/", HTTP_X_TENANT_ID=str(tenant.id))
        request.user = user

        middleware = TenantMiddleware(lambda r: Mock())
        middleware(request)

        assert request.tenant == tenant
        assert hasattr(request, "user_role")

    def test_middleware_with_query_param(self, tenant, user):
        factory = RequestFactory()
        request = factory.get(f"/api/test/?tenant_id={tenant.id}")
        request.user = user

        middleware = TenantMiddleware(lambda r: Mock())
        middleware(request)

        assert request.tenant == tenant
        assert hasattr(request, "user_role")

    def test_middleware_without_tenant_id(self, user):
        factory = RequestFactory()
        request = factory.get("/api/test/")
        request.user = user

        middleware = TenantMiddleware(lambda r: Mock())
        middleware(request)

        assert request.tenant is None
        assert request.user_role is None

    def test_middleware_with_invalid_tenant_id(self, user):
        factory = RequestFactory()
        request = factory.get("/api/test/", HTTP_X_TENANT_ID="invalid-id")
        request.user = user

        middleware = TenantMiddleware(lambda r: Mock())
        middleware(request)

        # SimpleLazyObject will return None when evaluated
        assert request.tenant is None

    def test_middleware_header_takes_precedence_over_query_param(self, tenant, user, tenant_factory):
        other_tenant = tenant_factory()
        factory = RequestFactory()
        request = factory.get(f"/api/test/?tenant_id={other_tenant.id}", HTTP_X_TENANT_ID=str(tenant.id))
        request.user = user

        middleware = TenantMiddleware(lambda r: Mock())
        middleware(request)

        # Header should take precedence
        assert request.tenant == tenant
        assert request.tenant != other_tenant
