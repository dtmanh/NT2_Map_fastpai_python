"""create table object_equipments

Revision ID: 4d4388d2285f
Revises: ac7fbaddcc34
Create Date: 2022-10-04 08:18:51.908057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d4388d2285f'
down_revision = 'ac7fbaddcc34'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'object_equipments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.VARCHAR(length=255), default=None, nullable=True),
        sa.Column('attributes', sa.JSON(), nullable=True),
        sa.Column('equipment_id', sa.Integer()),
        sa.Column('object_id', sa.Integer()),
        sa.Column('created_at', sa.DateTime(), default=None, nullable=True),
        sa.Column('updated_at', sa.DateTime(), default=None, nullable=True),
        sa.ForeignKeyConstraint(['equipment_id'], ['equipments.id'], name='object_equipments_equipment_id_fkey', ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_constraint(u'object_equipments_equipment_id_fkey', 'object_equipments', type_='foreignkey')
    op.drop_table('object_equipments')
