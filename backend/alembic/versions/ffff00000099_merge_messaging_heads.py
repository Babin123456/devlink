"""merge messaging heads

Revision ID: ffff00000099
Revises: 366aca8c8494, a1b2c3d4e5f8, ea6d6738e0b0, ffff00000004, voice_intro_url_001
Create Date: 2026-08-16 12:00:00.000000

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "ffff00000099"
down_revision: Union[str, Sequence[str], None] = (
    "366aca8c8494",
    "a1b2c3d4e5f8",
    "ea6d6738e0b0",
    "ffff00000004",
    "voice_intro_url_001",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
