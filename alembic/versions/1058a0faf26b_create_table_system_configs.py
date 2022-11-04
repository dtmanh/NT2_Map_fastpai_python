"""create_table_system_configs

Revision ID: 1058a0faf26b
Revises: 12cc8c8f5d04
Create Date: 2022-08-11 06:47:15.272864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1058a0faf26b'
down_revision = '12cc8c8f5d04'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'system_configs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('key_value', sa.Text(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_by', sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('system_configs')
