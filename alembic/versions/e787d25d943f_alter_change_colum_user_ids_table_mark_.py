"""alter change colum user_ids table mark map area

Revision ID: e787d25d943f
Revises: 82c272182a0d
Create Date: 2022-10-13 07:59:32.868945

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = 'e787d25d943f'
down_revision = '82c272182a0d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('mark_map_areas', 'user_ids')
    op.add_column('mark_map_areas', sa.Column('user_ids', JSONB(), default=True)) 


def downgrade() -> None:
    pass
