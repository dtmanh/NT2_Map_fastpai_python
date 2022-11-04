"""create table area profile

Revision ID: 0ddb0fd18b82
Revises: 7514e45c664d
Create Date: 2022-08-16 04:23:38.641373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ddb0fd18b82'
down_revision = '7514e45c664d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass
    # op.create_table(
    #     'area_profiles',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('area_id', sa.Integer),
    #     sa.Column('user_id', sa.Integer),
    #     sa.Column('name', sa.String(), nullable=True),
    #     sa.Column('type', sa.String(), nullable=True),
    #     sa.Column('lever', sa.Integer(), nullable=True),
    #     sa.Column('content', sa.Text(), default=False),
    #     sa.Column('created_at', sa.DateTime(), nullable=True),
    #     sa.Column('updated_at', sa.DateTime(), nullable=True),
    #     sa.Column('deleted_by', sa.String(), nullable=True),
    #     sa.Column('deleted_at', sa.DateTime(), nullable=True)
    # )

def downgrade() -> None:
    # op.drop_table('area_profiles')
    pass
