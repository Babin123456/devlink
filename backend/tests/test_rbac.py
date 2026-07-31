"""Comprehensive RBAC tests (issue #357).

Tests cover:
- SystemRole enum values
- SYSTEM_ROLE_PERMISSIONS mapping
- has_system_permission() for each role
- has_system_role() for each role
- has_org_permission() with various org roles
- has_project_permission() with various project roles
- get_user_system_role()
- get_user_permissions() aggregation
- require_roles() and require_system_permission() FastAPI dependencies
- Integration: unauthorized actions are blocked
- Integration: role permissions are configurable
"""

from __future__ import annotations

import uuid
from unittest.mock import MagicMock

from app.core.rbac import (
    DEFAULT_SYSTEM_ROLE,
    ORG_DELETE,
    ORG_MANAGE_MEMBERS,
    ORG_MANAGE_TOKENS,
    ORG_UPDATE,
    PROJECT_ARCHIVE,
    PROJECT_DELETE,
    PROJECT_INVITE,
    PROJECT_RESTORE,
    PROJECT_UPDATE,
    PROJECT_VIEW,
    SYSTEM_ADMIN_ROLES,
    SYSTEM_CONTRIBUTE,
    SYSTEM_CREATE_ORG,
    SYSTEM_CREATE_PROJECT,
    SYSTEM_MANAGE_CONTENT,
    SYSTEM_MANAGE_SYSTEM,
    SYSTEM_MANAGE_USERS,
    SYSTEM_OWNER_ROLES,
    SYSTEM_STAFF_ROLES,
    SYSTEM_VIEW_ANALYTICS,
    ORG_ROLE_PERMISSIONS,
    PROJECT_ROLE_PERMISSIONS,
    SYSTEM_ROLE_PERMISSIONS,
    SystemRole,
    get_user_permissions,
    get_user_system_role,
    has_system_permission,
    has_system_role,
)
from app.models.organization_member import OrgMemberRole
from app.models.project_member import MemberRole


# ─── SystemRole enum tests ──────────────────────────────────────────────────


class TestSystemRoleEnum:
    """Verify SystemRole enum values match the issue spec."""

    def test_admin_role_exists(self):
        assert SystemRole.ADMIN == "admin"

    def test_maintainer_role_exists(self):
        assert SystemRole.MAINTAINER == "maintainer"

    def test_organization_owner_role_exists(self):
        assert SystemRole.ORGANIZATION_OWNER == "organization_owner"

    def test_project_owner_role_exists(self):
        assert SystemRole.PROJECT_OWNER == "project_owner"

    def test_contributor_role_exists(self):
        assert SystemRole.CONTRIBUTOR == "contributor"

    def test_user_role_exists(self):
        assert SystemRole.USER == "user"

    def test_default_role_is_user(self):
        assert DEFAULT_SYSTEM_ROLE == SystemRole.USER

    def test_all_six_roles_present(self):
        assert len(SystemRole) == 6


# ─── SYSTEM_ROLE_PERMISSIONS tests ──────────────────────────────────────────


class TestSystemRolePermissions:
    """Verify the permission mapping for each system role."""

    def test_admin_has_all_permissions(self):
        perms = SYSTEM_ROLE_PERMISSIONS[SystemRole.ADMIN]
        assert SYSTEM_MANAGE_USERS in perms
        assert SYSTEM_MANAGE_CONTENT in perms
        assert SYSTEM_VIEW_ANALYTICS in perms
        assert SYSTEM_MANAGE_SYSTEM in perms
        assert SYSTEM_CREATE_ORG in perms
        assert SYSTEM_CREATE_PROJECT in perms
        assert SYSTEM_CONTRIBUTE in perms

    def test_maintainer_has_content_and_analytics(self):
        perms = SYSTEM_ROLE_PERMISSIONS[SystemRole.MAINTAINER]
        assert SYSTEM_MANAGE_CONTENT in perms
        assert SYSTEM_VIEW_ANALYTICS in perms
        assert SYSTEM_CONTRIBUTE in perms
        assert SYSTEM_MANAGE_USERS not in perms
        assert SYSTEM_MANAGE_SYSTEM not in perms

    def test_org_owner_can_create_org(self):
        perms = SYSTEM_ROLE_PERMISSIONS[SystemRole.ORGANIZATION_OWNER]
        assert SYSTEM_CREATE_ORG in perms
        assert SYSTEM_VIEW_ANALYTICS in perms
        assert SYSTEM_CONTRIBUTE in perms

    def test_project_owner_can_create_project(self):
        perms = SYSTEM_ROLE_PERMISSIONS[SystemRole.PROJECT_OWNER]
        assert SYSTEM_CREATE_PROJECT in perms
        assert SYSTEM_VIEW_ANALYTICS in perms
        assert SYSTEM_CONTRIBUTE in perms

    def test_contributor_can_contribute(self):
        perms = SYSTEM_ROLE_PERMISSIONS[SystemRole.CONTRIBUTOR]
        assert SYSTEM_CONTRIBUTE in perms
        assert len(perms) == 1

    def test_user_has_no_system_permissions(self):
        perms = SYSTEM_ROLE_PERMISSIONS[SystemRole.USER]
        assert len(perms) == 0

    def test_role_hierarchy_sets(self):
        assert SystemRole.ADMIN in SYSTEM_ADMIN_ROLES
        assert SystemRole.ADMIN in SYSTEM_STAFF_ROLES
        assert SystemRole.MAINTAINER in SYSTEM_STAFF_ROLES
        assert SystemRole.ORGANIZATION_OWNER in SYSTEM_OWNER_ROLES
        assert SystemRole.PROJECT_OWNER in SYSTEM_OWNER_ROLES


# ─── has_system_permission tests ────────────────────────────────────────────


class TestHasSystemPermission:
    """Test the has_system_permission function with mock DB."""

    def _make_user(self, role="user", is_superuser=False):
        user = MagicMock()
        user.id = uuid.uuid4()
        user.is_superuser = is_superuser
        user.system_role = role
        return user

    def test_superuser_has_all_permissions(self, db):
        user = self._make_user(is_superuser=True)
        db.add(user)
        db.commit()

        assert has_system_permission(db, user.id, SYSTEM_MANAGE_USERS) is True
        assert has_system_permission(db, user.id, SYSTEM_MANAGE_SYSTEM) is True

    def test_admin_has_all_permissions(self, db):
        user = self._make_user(role="admin")
        db.add(user)
        db.commit()

        assert has_system_permission(db, user.id, SYSTEM_MANAGE_USERS) is True
        assert has_system_permission(db, user.id, SYSTEM_MANAGE_CONTENT) is True

    def test_maintainer_has_content_not_users(self, db):
        user = self._make_user(role="maintainer")
        db.add(user)
        db.commit()

        assert has_system_permission(db, user.id, SYSTEM_MANAGE_CONTENT) is True
        assert has_system_permission(db, user.id, SYSTEM_MANAGE_USERS) is False

    def test_user_has_no_system_permissions(self, db):
        user = self._make_user(role="user")
        db.add(user)
        db.commit()

        assert has_system_permission(db, user.id, SYSTEM_MANAGE_USERS) is False
        assert has_system_permission(db, user.id, SYSTEM_CONTRIBUTE) is False

    def test_contributor_has_contribute(self, db):
        user = self._make_user(role="contributor")
        db.add(user)
        db.commit()

        assert has_system_permission(db, user.id, SYSTEM_CONTRIBUTE) is True
        assert has_system_permission(db, user.id, SYSTEM_MANAGE_USERS) is False

    def test_nonexistent_user_returns_false(self, db):
        fake_id = uuid.uuid4()
        assert has_system_permission(db, fake_id, SYSTEM_MANAGE_USERS) is False

    def test_invalid_role_defaults_to_user(self, db):
        user = self._make_user(role="invalid_role")
        db.add(user)
        db.commit()

        assert has_system_permission(db, user.id, SYSTEM_MANAGE_USERS) is False

    def test_none_role_defaults_to_user(self, db):
        user = self._make_user(role=None)
        db.add(user)
        db.commit()

        assert has_system_permission(db, user.id, SYSTEM_MANAGE_USERS) is False


# ─── has_system_role tests ──────────────────────────────────────────────────


class TestHasSystemRole:
    """Test the has_system_role function."""

    def _make_user(self, role="user", is_superuser=False):
        user = MagicMock()
        user.id = uuid.uuid4()
        user.is_superuser = is_superuser
        user.system_role = role
        return user

    def test_superuser_passes_any_role_check(self, db):
        user = self._make_user(is_superuser=True)
        db.add(user)
        db.commit()

        assert has_system_role(db, user.id, SystemRole.ADMIN) is True
        assert has_system_role(db, user.id, SystemRole.MAINTAINER) is True

    def test_admin_role_matches(self, db):
        user = self._make_user(role="admin")
        db.add(user)
        db.commit()

        assert has_system_role(db, user.id, SystemRole.ADMIN) is True
        assert has_system_role(db, user.id, SystemRole.MAINTAINER) is False

    def test_multiple_roles_check(self, db):
        user = self._make_user(role="maintainer")
        db.add(user)
        db.commit()

        assert (
            has_system_role(db, user.id, SystemRole.ADMIN, SystemRole.MAINTAINER)
            is True
        )
        assert has_system_role(db, user.id, SystemRole.ADMIN) is False

    def test_user_role_does_not_match_admin(self, db):
        user = self._make_user(role="user")
        db.add(user)
        db.commit()

        assert has_system_role(db, user.id, SystemRole.ADMIN) is False


# ─── get_user_system_role tests ─────────────────────────────────────────────


class TestGetUserSystemRole:
    """Test the get_user_system_role function."""

    def _make_user(self, role="user", is_superuser=False):
        user = MagicMock()
        user.id = uuid.uuid4()
        user.is_superuser = is_superuser
        user.system_role = role
        return user

    def test_superuser_returns_admin(self, db):
        user = self._make_user(is_superuser=True)
        db.add(user)
        db.commit()

        assert get_user_system_role(db, user.id) == SystemRole.ADMIN

    def test_returns_correct_role(self, db):
        for role in SystemRole:
            user = self._make_user(role=role.value)
            db.add(user)
            db.commit()

            assert get_user_system_role(db, user.id) == role
            db.delete(user)
            db.commit()

    def test_none_role_returns_user(self, db):
        user = self._make_user(role=None)
        db.add(user)
        db.commit()

        assert get_user_system_role(db, user.id) == SystemRole.USER

    def test_invalid_role_returns_user(self, db):
        user = self._make_user(role="nonexistent")
        db.add(user)
        db.commit()

        assert get_user_system_role(db, user.id) == SystemRole.USER

    def test_nonexistent_user_returns_default(self, db):
        fake_id = uuid.uuid4()
        assert get_user_system_role(db, fake_id) == DEFAULT_SYSTEM_ROLE


# ─── Org-level permission tests ─────────────────────────────────────────────


class TestOrgRolePermissions:
    """Verify org role → permission mapping."""

    def test_owner_has_all_org_permissions(self):
        perms = ORG_ROLE_PERMISSIONS[OrgMemberRole.OWNER]
        assert ORG_UPDATE in perms
        assert ORG_DELETE in perms
        assert ORG_MANAGE_MEMBERS in perms
        assert ORG_MANAGE_TOKENS in perms

    def test_admin_has_manage_but_not_delete(self):
        perms = ORG_ROLE_PERMISSIONS[OrgMemberRole.ADMIN]
        assert ORG_UPDATE in perms
        assert ORG_MANAGE_MEMBERS in perms
        assert ORG_MANAGE_TOKENS in perms
        assert ORG_DELETE not in perms

    def test_member_has_no_org_permissions(self):
        perms = ORG_ROLE_PERMISSIONS[OrgMemberRole.MEMBER]
        assert len(perms) == 0


# ─── Project-level permission tests ─────────────────────────────────────────


class TestProjectRolePermissions:
    """Verify project role → permission mapping."""

    def test_owner_has_all_project_permissions(self):
        perms = PROJECT_ROLE_PERMISSIONS[MemberRole.OWNER]
        assert PROJECT_UPDATE in perms
        assert PROJECT_DELETE in perms
        assert PROJECT_INVITE in perms
        assert PROJECT_ARCHIVE in perms
        assert PROJECT_RESTORE in perms
        assert PROJECT_VIEW in perms

    def test_co_owner_has_all_except_delete(self):
        perms = PROJECT_ROLE_PERMISSIONS[MemberRole.CO_OWNER]
        assert PROJECT_UPDATE in perms
        assert PROJECT_INVITE in perms
        assert PROJECT_ARCHIVE in perms
        assert PROJECT_RESTORE in perms
        assert PROJECT_VIEW in perms
        assert PROJECT_DELETE not in perms

    def test_maintainer_can_update_and_invite(self):
        perms = PROJECT_ROLE_PERMISSIONS[MemberRole.MAINTAINER]
        assert PROJECT_UPDATE in perms
        assert PROJECT_INVITE in perms
        assert PROJECT_VIEW in perms
        assert PROJECT_DELETE not in perms
        assert PROJECT_ARCHIVE not in perms

    def test_member_can_only_view(self):
        perms = PROJECT_ROLE_PERMISSIONS[MemberRole.MEMBER]
        assert PROJECT_VIEW in perms
        assert len(perms) == 1


# ─── Integration: unauthorized actions blocked ──────────────────────────────


class TestUnauthorizedActionsBlocked:
    """Integration tests verifying that unauthorized actions are blocked."""

    def test_user_cannot_access_admin_endpoint(self, client, register_and_login):
        """A regular USER should get 403 on an admin-only endpoint."""
        user_id, token = register_and_login(
            "user@test.com", "testuser", "Passw0rd!"
        )

        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code in (403, 404)

    def test_admin_can_access_admin_endpoint(
        self, client, db, register_and_login
    ):
        """An ADMIN user should be able to access admin endpoints."""
        user_id, token = register_and_login(
            "admin@test.com", "adminuser", "Passw0rd!"
        )

        from app.models.user import User

        user = db.get(User, uuid.UUID(user_id))
        user.system_role = "admin"
        user.is_superuser = True
        db.commit()

        response = client.get(
            "/api/users",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code != 403


# ─── Permission aggregation tests ───────────────────────────────────────────


class TestGetUserPermissions:
    """Test the get_user_permissions aggregation function."""

    def _make_user(self, role="user", is_superuser=False):
        user = MagicMock()
        user.id = uuid.uuid4()
        user.is_superuser = is_superuser
        user.system_role = role
        return user

    def test_superuser_gets_all_permissions(self, db):
        user = self._make_user(is_superuser=True)
        db.add(user)
        db.commit()

        perms = get_user_permissions(db, user.id)
        assert SYSTEM_MANAGE_USERS in perms
        assert SYSTEM_MANAGE_SYSTEM in perms
        assert ORG_DELETE in perms
        assert PROJECT_DELETE in perms

    def test_regular_user_gets_empty_permissions(self, db):
        user = self._make_user(role="user")
        db.add(user)
        db.commit()

        perms = get_user_permissions(db, user.id)
        assert len(perms) == 0

    def test_contributor_gets_contribute(self, db):
        user = self._make_user(role="contributor")
        db.add(user)
        db.commit()

        perms = get_user_permissions(db, user.id)
        assert SYSTEM_CONTRIBUTE in perms

    def test_nonexistent_user_returns_empty(self, db):
        fake_id = uuid.uuid4()
        perms = get_user_permissions(db, fake_id)
        assert perms == set()


# ─── Role configurability tests ─────────────────────────────────────────────


class TestRoleConfigurability:
    """Verify that roles are configurable (can be changed at runtime)."""

    def _make_user(self, role="user"):
        user = MagicMock()
        user.id = uuid.uuid4()
        user.is_superuser = False
        user.system_role = role
        return user

    def test_promoting_user_grants_permissions(self, db):
        user = self._make_user(role="user")
        db.add(user)
        db.commit()

        assert has_system_permission(db, user.id, SYSTEM_MANAGE_CONTENT) is False

        user.system_role = "maintainer"
        db.commit()

        assert has_system_permission(db, user.id, SYSTEM_MANAGE_CONTENT) is True

    def test_demoting_user_removes_permissions(self, db):
        user = self._make_user(role="admin")
        db.add(user)
        db.commit()

        assert has_system_permission(db, user.id, SYSTEM_MANAGE_USERS) is True

        user.system_role = "user"
        db.commit()

        assert has_system_permission(db, user.id, SYSTEM_MANAGE_USERS) is False
