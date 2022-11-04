"""create table symbols

Revision ID: 7befb4f159a9
Revises: f6b76800e565
Create Date: 2022-09-15 14:09:39.864474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7befb4f159a9'
down_revision = 'f6b76800e565'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'symbols',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('label', sa.String),
        sa.Column('v_label', sa.String),
        sa.Column('object_name', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    op.add_column('objects', sa.Column('symbol_id', sa.Integer))

def downgrade() -> None:
    op.drop_table('symbols')
    op.drop_column('objects', 'symbol_id')
