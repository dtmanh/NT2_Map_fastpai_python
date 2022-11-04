"""create_table_user_layer

Revision ID: 7514e45c664d
Revises: 9fe9ae20c9c8
Create Date: 2022-08-16 04:15:16.140401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7514e45c664d'
down_revision = '9fe9ae20c9c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user_layers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('layer_id', sa.Text, unique=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('tags', sa.Text()),
        sa.Column('geometry', sa.Text(), default=False),
        sa.Column('properties', sa.Text(), default=False),
        sa.Column('meta_data', sa.Text(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

def downgrade() -> None:
    op.drop_table('user_layers')
