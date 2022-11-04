"""alter table objects add column tags

Revision ID: 2ffa268f02e5
Revises: c8e4678134f4
Create Date: 2022-09-13 14:52:48.267764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ffa268f02e5'
down_revision = 'c8e4678134f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('objects', sa.Column('tags', sa.Text))


def downgrade() -> None:
    op.drop_column('objects', 'tags')

