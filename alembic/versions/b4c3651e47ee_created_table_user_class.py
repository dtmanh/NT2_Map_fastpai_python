"""created_table_user_class

Revision ID: b4c3651e47ee
Revises: 4fe7f64e5916
Create Date: 2022-08-30 16:04:26.831787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4c3651e47ee'
down_revision = '4fe7f64e5916'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.create_table(
    #     'user_class',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('layer_id', sa.Text(), unique=True),
    #     sa.Column('name', sa.VARCHAR(length=150), nullable=True),
    #     sa.Column('data', sa.Text(), default=False),
    #     sa.Column('user_id', sa.Integer()),
    #     sa.Column('created_at', sa.DateTime(), nullable=True),
    #     sa.Column('updated_at', sa.DateTime(), nullable=True)
    # )
    pass

def downgrade() -> None:
    # op.drop_table('user_class')
    pass