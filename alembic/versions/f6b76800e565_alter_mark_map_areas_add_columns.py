"""alter mark map areas add columns

Revision ID: f6b76800e565
Revises: 2ffa268f02e5
Create Date: 2022-09-14 01:36:14.169274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6b76800e565'
down_revision = '2ffa268f02e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('mark_map_areas', sa.Column('type', sa.String))
    op.add_column('mark_map_areas', sa.Column('code', sa.Text))
    op.add_column('mark_map_areas', sa.Column('description', sa.Text))
    op.add_column('mark_map_areas', sa.Column('active', sa.Boolean, default=True))
    op.add_column('mark_map_areas', sa.Column('user_ids', sa.Text))

def downgrade() -> None:
    op.drop_column('mark_map_areas', 'type')
    op.drop_column('mark_map_areas', 'code')
    op.drop_column('mark_map_areas', 'description')
    op.drop_column('mark_map_areas', 'active')
    op.drop_column('mark_map_areas', 'user_ids')
