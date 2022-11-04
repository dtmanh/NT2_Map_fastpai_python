"""create_table_roles

Revision ID: 703548246041
Revises: 1282cd823976
Create Date: 2022-08-11 03:42:49.916120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '703548246041'
down_revision = '1282cd823976'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_by', sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('roles')
