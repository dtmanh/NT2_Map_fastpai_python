"""create table object_layers

Revision ID: 3cc304795ce6
Revises: b4c3651e47ee
Create Date: 2022-09-06 10:30:36.286411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cc304795ce6'
down_revision = 'b4c3651e47ee'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        'object_layers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.VARCHAR(length=150), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('object_layers')
