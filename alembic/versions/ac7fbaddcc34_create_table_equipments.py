"""create table equipments

Revision ID: ac7fbaddcc34
Revises: 786720bb79bb
Create Date: 2022-10-04 08:16:44.027264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac7fbaddcc34'
down_revision = '786720bb79bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'equipments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.VARCHAR(length=255), nullable=True),
        sa.Column('code', sa.VARCHAR(length=30), default=None, nullable=True),
        sa.Column('attributes', sa.JSON(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=None, nullable=True),
        sa.Column('updated_at', sa.DateTime(), default=None, nullable=True)
    )


def downgrade() -> None:
    op.drop_table('equipments')