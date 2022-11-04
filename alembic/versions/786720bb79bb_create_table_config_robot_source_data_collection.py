"""create table setup robot data collectors

Revision ID: 786720bb79bb
Revises: 547d1992502a
Create Date: 2022-10-04 07:42:18.502043

"""
from token import COMMENT
from tokenize import Comment
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '786720bb79bb'
down_revision = '547d1992502a'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'config_robot_source_data_collections',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.VARCHAR(length=255), nullable=True),
        sa.Column('description', sa.VARCHAR(length=255), default=None, nullable=True),
        sa.Column('type_data', sa.Enum('satellite_image', 'data_gis', 'satellite_aster', name='config_robot_source_data_collection_type_data', create_type=False), nullable=True),
        sa.Column('source_id', sa.Integer(), default=None, nullable=True),
        sa.Column('priority', sa.Integer(), default=None, nullable=True),
        sa.Column('frequency', sa.Integer(), nullable=True),
        sa.Column('attribute', sa.JSON(), default=None, nullable=True),
        sa.Column('geometry', sa.JSON(), default=None, nullable=True),
        sa.Column('is_check', sa.Boolean(), default=False),
        sa.Column('start_time', sa.DateTime(), default=None, nullable=True),
        sa.Column('end_time', sa.DateTime(), default=None, nullable=True),
        sa.Column('status', sa.Enum('draft', 'approve', 'published', name='config_robot_source_data_collection_status', create_type=False), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=None, nullable=True),
        sa.Column('updated_at', sa.DateTime(), default=None, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='config_robot_source_data_collection_user_id_fkey', ondelete="CASCADE"),
    )

def downgrade() -> None:
    op.drop_constraint(u'config_robot_source_data_collection_user_id_fkey', 'config_robot_source_data_collections', type_='foreignkey')
    op.drop_table('config_robot_source_data_collections')
    postgresql.ENUM('satellite_image', 'data_gis', 'satellite_aster', name='config_robot_source_data_collection_type_data').drop(op.get_bind())
    postgresql.ENUM('draft', 'approve', 'published', name=u'config_robot_source_data_collection_status').drop(op.get_bind())