"""create_table_system_logs

Revision ID: 12cc8c8f5d04
Revises: 5607ef50ce22
Create Date: 2022-08-11 06:40:55.740915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12cc8c8f5d04'
down_revision = '5607ef50ce22'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'system_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column('action', sa.String(), nullable=True),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('method', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('ip', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('accept', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('warehouse', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_by', sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('system_logs')
