"""create_table_permissions

Revision ID: c76a6e068842
Revises: 703548246041
Create Date: 2022-08-11 06:07:45.229751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c76a6e068842'
down_revision = '703548246041'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('key', sa.String(255), nullable=True),
        sa.Column('module', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_by', sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('permissions')
