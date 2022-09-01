"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


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
    ${downgrades if downgrades else "pass"}
