"""alter add column table config_robot_souce_data

Revision ID: 322c48d8bed6
Revises: e7f178b70888
Create Date: 2022-10-11 08:47:44.600412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '322c48d8bed6'
down_revision = 'e7f178b70888'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('config_robot_source_data_collections', sa.Column('properties', sa.JSON)) 


def downgrade() -> None:
    op.drop_column('config_robot_source_data_collections', 'properties')
