"""create table user fillter config

Revision ID: def698d5304e
Revises: 0ddb0fd18b82
Create Date: 2022-08-16 09:40:08.274337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'def698d5304e'
down_revision = '0ddb0fd18b82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user_fillter_configs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column('data_fillter', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

def downgrade() -> None:
    op.drop_table('user_fillter_configs')
