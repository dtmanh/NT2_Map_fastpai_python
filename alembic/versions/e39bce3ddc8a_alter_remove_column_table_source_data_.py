"""alter remove column table source data collections

Revision ID: e39bce3ddc8a
Revises: e787d25d943f
Create Date: 2022-10-14 06:43:26.374830

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import engine_from_config
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision = 'e39bce3ddc8a'
down_revision = 'e787d25d943f'
branch_labels = None
depends_on = None

def _table_has_column(table, column):
    config = op.get_context().config
    engine = engine_from_config(
        config.get_section(config.config_ini_section), prefix='sqlalchemy.')
    insp = reflection.Inspector.from_engine(engine)
    has_column = False
    for col in insp.get_columns(table):
        if column not in col['name']:
            continue
        has_column = True
    return has_column

def upgrade() -> None:
    if _table_has_column('source_data_collections', 'frequency'):
        op.drop_column('source_data_collections', 'frequency'),
    if _table_has_column('source_data_collections', 'attributes'):
        op.drop_column('source_data_collections', 'attributes'),
    if _table_has_column('source_data_collections', 'is_check'):
        op.drop_column('source_data_collections', 'is_check'),
    if _table_has_column('source_data_collections', 'start_time'):
        op.drop_column('source_data_collections', 'start_time'),
    if _table_has_column('source_data_collections', 'end_time'):
        op.drop_column('source_data_collections', 'end_time')


def downgrade() -> None:
    pass
