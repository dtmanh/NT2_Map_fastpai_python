"""create table objects

Revision ID: c8e4678134f4
Revises: 3cc304795ce6
Create Date: 2022-09-06 11:04:34.509358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8e4678134f4'
down_revision = '3cc304795ce6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'objects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('object_layer_id', sa.Integer, sa.ForeignKey("object_layers.id", ondelete="CASCADE")),
        sa.Column('user_id', sa.Integer),
        sa.Column('name', sa.Text()),
        sa.Column('description', sa.Text()),
        sa.Column('image', sa.Text()),
        sa.Column('properties', sa.Text(), default=False),
        sa.Column('geometry', sa.Text(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('objects')
