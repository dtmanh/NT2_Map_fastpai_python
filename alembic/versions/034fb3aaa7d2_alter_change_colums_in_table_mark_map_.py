"""alter change colums in table mark map area

Revision ID: 034fb3aaa7d2
Revises: 4d4388d2285f
Create Date: 2022-10-10 07:18:06.686225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '034fb3aaa7d2'
down_revision = '4d4388d2285f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('mark_map_areas', 'user_ids')
    

def downgrade() -> None:
    op.add_column('mark_map_areas', sa.Column('user_ids', sa.Text))
