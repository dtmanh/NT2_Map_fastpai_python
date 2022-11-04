"""create table object profiles

Revision ID: 4fe7f64e5916
Revises: def698d5304e
Create Date: 2022-08-25 09:25:55.681491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fe7f64e5916'
down_revision = 'def698d5304e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.create_table(
    #     'object_profiles',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('name', sa.String(), nullable=True),
    #     sa.Column('description', sa.String(), nullable=True),
    #     sa.Column('content', sa.Text(), nullable=True),
    #     sa.Column('geometry', sa.Text(), nullable=True),
    #     sa.Column('properties', sa.Text(), nullable=True),
    #     sa.Column('type', sa.String(), default=False),
    #     sa.Column('user_id', sa.Integer),
    #     sa.Column('created_at', sa.DateTime(), nullable=True),
    #     sa.Column('updated_at', sa.DateTime(), nullable=True),
    # )
    pass

def downgrade() -> None:
    # op.drop_table('object_profiles')
    pass