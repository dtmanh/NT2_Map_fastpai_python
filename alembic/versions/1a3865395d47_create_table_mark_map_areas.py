"""create_table_mark_map_areas

Revision ID: 1a3865395d47
Revises: 1058a0faf26b
Create Date: 2022-08-11 06:51:38.095521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a3865395d47'
down_revision = '1058a0faf26b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'mark_map_areas',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String()),
        sa.Column('geometry', sa.Text(), nullable=False),
        sa.Column('properties', sa.Text(), default=False),
        sa.Column('meta_data', sa.Text(), default=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('mark_map_areas')
