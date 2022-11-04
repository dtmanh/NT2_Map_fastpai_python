"""create_table_role_permission

Revision ID: 5607ef50ce22
Revises: c76a6e068842
Create Date: 2022-08-11 06:16:11.317785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5607ef50ce22'
down_revision = 'c76a6e068842'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'role_permission',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey("roles.id", ondelete="CASCADE"), nullable=False),
        sa.Column('permission_id', sa.Integer(), sa.ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('role_permission')
