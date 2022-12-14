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
    op.create_unique_constraint(constraint_name="unique_name", table_name="script", columns=["name"])


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
    op.drop_constraint(constraint_name="unique_name", table_name="script")