"""create_table_history_searchs

Revision ID: 9fe9ae20c9c8
Revises: 1a3865395d47
Create Date: 2022-08-15 09:50:40.274759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fe9ae20c9c8'
down_revision = '1a3865395d47'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'history_searchs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column('data_search', sa.Text())
    )

def downgrade() -> None:
    op.drop_table('history_searchs')
