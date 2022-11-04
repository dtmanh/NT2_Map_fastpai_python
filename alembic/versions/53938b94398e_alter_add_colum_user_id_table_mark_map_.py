"""alter add colum user_id table mark map area

Revision ID: 53938b94398e
Revises: 034fb3aaa7d2
Create Date: 2022-10-11 08:37:31.419322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53938b94398e'
down_revision = '034fb3aaa7d2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('mark_map_areas', sa.Column('user_ids', sa.JSON)) 


def downgrade() -> None:
    op.drop_column('mark_map_areas', 'user_ids')
