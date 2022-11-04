"""alter table source_data_collections

Revision ID: 642f24887401
Revises: 322c48d8bed6
Create Date: 2022-10-12 02:52:13.832068

"""
from email.policy import default
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '642f24887401'
down_revision = '322c48d8bed6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('source_data_collections', sa.Column('is_available', sa.Boolean, default=False, nullable=True))


def downgrade() -> None:
    op.drop_column('source_data_collections', 'is_available')
