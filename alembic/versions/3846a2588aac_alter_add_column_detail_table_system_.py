"""alter add column detail table system logs

Revision ID: 3846a2588aac
Revises: 3de26d0792f4
Create Date: 2022-10-18 02:52:07.823449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3846a2588aac'
down_revision = '3de26d0792f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('system_logs', sa.Column('detail', sa.Text, default=False))


def downgrade() -> None:
    op.drop_column('system_logs', 'detail')
