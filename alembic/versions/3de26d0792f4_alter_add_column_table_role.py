"""alter add column table role

Revision ID: 3de26d0792f4
Revises: e39bce3ddc8a
Create Date: 2022-10-17 07:35:55.640029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3de26d0792f4'
down_revision = 'e39bce3ddc8a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('roles', sa.Column('is_system', sa.Boolean, default=False))


def downgrade() -> None:
    op.drop_column('roles', 'is_system')
