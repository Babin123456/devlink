"""add full text search indexes

Revision ID: c5d6e7f8a9b0
Revises: b1c2d3e4f5a6
Create Date: 2026-07-26 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op


revision: str = "c5d6e7f8a9b0"
down_revision: Union[str, None] = "b1c2d3e4f5a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # PostgreSQL GIN functional indexes on to_tsvector for full-text search
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_users_fts ON users USING gin(
            to_tsvector('english',
                coalesce(username, '') || ' ' ||
                coalesce(first_name, '') || ' ' ||
                coalesce(last_name, '') || ' ' ||
                coalesce(role, '') || ' ' ||
                coalesce(headline, '')
            )
        );
        """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_projects_fts ON projects USING gin(
            to_tsvector('english',
                coalesce(title, '') || ' ' ||
                coalesce(tagline, '') || ' ' ||
                coalesce(description, '') || ' ' ||
                coalesce(tech_stack, '')
            )
        );
        """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_organizations_fts ON organizations USING gin(
            to_tsvector('english',
                coalesce(name, '') || ' ' ||
                coalesce(slug, '') || ' ' ||
                coalesce(description, '') || ' ' ||
                coalesce(location, '')
            )
        );
        """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_skills_fts ON skills USING gin(
            to_tsvector('english',
                coalesce(name, '') || ' ' ||
                coalesce(normalized_name, '') || ' ' ||
                coalesce(category, '') || ' ' ||
                coalesce(description, '')
            )
        );
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_users_fts;")
    op.execute("DROP INDEX IF EXISTS idx_projects_fts;")
    op.execute("DROP INDEX IF EXISTS idx_organizations_fts;")
    op.execute("DROP INDEX IF EXISTS idx_skills_fts;")
