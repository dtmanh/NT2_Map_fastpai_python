"""create table Source_data_collections

Revision ID: 547d1992502a
Revises: 7befb4f159a9
Create Date: 2022-10-04 07:24:17.387827

"""
from alembic import op
import sqlalchemy as sa

from app.core.constant.constant import PRIORITY_DEFAULT


# revision identifiers, used by Alembic.
revision = '547d1992502a'
down_revision = '7befb4f159a9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'source_data_collections',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.VARCHAR(length=255), unique=True, nullable=True),
        sa.Column('description', sa.VARCHAR(length=255), default=None, nullable=True),
        sa.Column('url', sa.VARCHAR(length=255), default=None, nullable=True),
        sa.Column('priority', sa.Integer(), default=PRIORITY_DEFAULT, nullable=True),
        sa.Column('frequency', sa.Integer(), nullable=True),
        sa.Column('attributes', sa.JSON(), nullable=True),
        sa.Column('is_check', sa.Boolean(), default=False),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='source_data_collection_user_id_fkey', ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_constraint(u'source_data_collection_user_id_fkey', 'source_data_collections', type_='foreignkey')
    op.drop_table('source_data_collections')
