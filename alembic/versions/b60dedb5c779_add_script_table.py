"""add script table

Revision ID: b60dedb5c779
Revises: 9c313f035956
Create Date: 2022-08-31 15:25:39.528397

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b60dedb5c779'
down_revision = '9c313f035956'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'script',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
        sa.Column('filepath', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False)
    )


def downgrade() -> None:
    pass
