"""alter add column table equipments

Revision ID: e7f178b70888
Revises: 53938b94398e
Create Date: 2022-10-11 08:43:30.845277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7f178b70888'
down_revision = '53938b94398e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('equipments', sa.Column('radius', sa.FLOAT)) 
    op.add_column('object_equipments', sa.Column('quantity', sa.INTEGER)) 
    op.add_column('object_equipments', sa.Column('radius', sa.FLOAT)) 


def downgrade() -> None:
    op.drop_column('equipments', 'radius')
    op.drop_column('object_equipments', 'radius')
    op.drop_column('object_equipments', 'quantity')
