"""Add microsoft_id to user

Revision ID: ffff00000002
Revises: ffff00000001
Create Date: 2026-08-03

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "ffff00000002"
down_revision: Union[str, Sequence[str], None] = "ffff00000001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("microsoft_id", sa.String(length=100), nullable=True))
    op.create_unique_constraint(None, "users", ["microsoft_id"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
    op.drop_column("users", "microsoft_id")
