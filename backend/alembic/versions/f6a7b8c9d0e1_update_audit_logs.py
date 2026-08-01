"""update audit logs

Revision ID: f6a7b8c9d0e1
Revises: c14aa06f723a
Create Date: 2026-07-30 14:35:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f6a7b8c9d0e1"
down_revision = "c14aa06f723a"


def upgrade() -> None:
    # Rename columns
    op.alter_column("audit_logs", "user_id", new_column_name="actor_id")
    op.alter_column("audit_logs", "resource_type", new_column_name="entity_type")
    op.alter_column("audit_logs", "resource_id", new_column_name="entity_id")

    # Add new columns
    op.add_column(
        "audit_logs",
        sa.Column("target_user_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "audit_logs",
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "audit_logs",
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "audit_logs",
        sa.Column("old_values", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.add_column(
        "audit_logs",
        sa.Column("new_values", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.add_column(
        "audit_logs",
        sa.Column(
            "metadata_info", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )

    # Add foreign keys
    op.create_foreign_key(
        "fk_audit_logs_target_user_id",
        "audit_logs",
        "users",
        ["target_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_audit_logs_project_id",
        "audit_logs",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_audit_logs_organization_id",
        "audit_logs",
        "organizations",
        ["organization_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # Create indexes
    op.create_index(
        op.f("ix_audit_logs_target_user_id"),
        "audit_logs",
        ["target_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_audit_logs_project_id"), "audit_logs", ["project_id"], unique=False
    )
    op.create_index(
        op.f("ix_audit_logs_organization_id"),
        "audit_logs",
        ["organization_id"],
        unique=False,
    )


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f("ix_audit_logs_organization_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_project_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_target_user_id"), table_name="audit_logs")

    # Drop foreign keys
    op.drop_constraint(
        "fk_audit_logs_organization_id", "audit_logs", type_="foreignkey"
    )
    op.drop_constraint("fk_audit_logs_project_id", "audit_logs", type_="foreignkey")
    op.drop_constraint("fk_audit_logs_target_user_id", "audit_logs", type_="foreignkey")

    # Drop new columns
    op.drop_column("audit_logs", "metadata_info")
    op.drop_column("audit_logs", "new_values")
    op.drop_column("audit_logs", "old_values")
    op.drop_column("audit_logs", "organization_id")
    op.drop_column("audit_logs", "project_id")
    op.drop_column("audit_logs", "target_user_id")

    # Rename back columns
    op.alter_column("audit_logs", "entity_id", new_column_name="resource_id")
    op.alter_column("audit_logs", "entity_type", new_column_name="resource_type")
    op.alter_column("audit_logs", "actor_id", new_column_name="user_id")
