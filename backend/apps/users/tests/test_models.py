import pytest

from core.acl.helpers import commonGroups

from .. import models

pytestmark = pytest.mark.django_db


class TestUser:
    def test_has_group_returns_false(self, user: models.User, group_factory):
        admin_group = group_factory(name=commonGroups.Admin)

        user.groups.remove(admin_group)

        assert not user.has_group(commonGroups.Admin)

    def test_has_group_returns_true(self, user: models.User, group_factory):
        admin_group = group_factory(name=commonGroups.Admin)

        user.groups.add(admin_group)

        assert user.has_group(commonGroups.Admin)
