"""add unique constraint

Revision ID: 9a717445c336
Revises: b60dedb5c779
Create Date: 2022-09-11 02:39:42.951703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a717445c336'
down_revision = 'b60dedb5c779'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(constraint_name="unique_name", table_name="script", columns=["name"])


def downgrade() -> None:
    pass
    op.drop_constraint(constraint_name="unique_name", table_name="script")