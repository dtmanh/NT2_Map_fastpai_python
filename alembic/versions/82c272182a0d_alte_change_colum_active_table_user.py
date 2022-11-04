"""alte change colum active table user

Revision ID: 82c272182a0d
Revises: 642f24887401
Create Date: 2022-10-13 06:41:33.985522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82c272182a0d'
down_revision = '642f24887401'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users', 'active')
    op.add_column('users', sa.Column('active', sa.Boolean(), default=True)) 
    

def downgrade() -> None:
    pass