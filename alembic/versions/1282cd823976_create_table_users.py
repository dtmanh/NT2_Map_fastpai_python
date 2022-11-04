"""create_table_users

Revision ID: 1282cd823976
Revises: 
Create Date: 2022-08-11 02:24:02.005041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1282cd823976'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('role_id', sa.Integer, nullable=True),
        sa.Column('full_name', sa.VARCHAR(length=150), nullable=True),
        sa.Column('first_name', sa.VARCHAR(length=150), nullable=True),
        sa.Column('last_name', sa.String(length=150), nullable=True),
        sa.Column('email', sa.String(length=150), unique=True, nullable=False),
        sa.Column('phone', sa.String(length=12), unique=True, nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('partner_unit', sa.String(), nullable=True),
        sa.Column('note', sa.String(), nullable=True),
        sa.Column('is_online', sa.Boolean(), default=False),
        sa.Column('active', sa.String(), nullable=True),
        sa.Column('expired_time', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_by', sa.String(), nullable=True),
    )

def downgrade() -> None:
    op.drop_table('users')
