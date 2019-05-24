"""empty message

Revision ID: 1a0c0c972818
Revises: 96d3e8caaf8d
Create Date: 2019-05-14 13:42:10.991703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a0c0c972818'
down_revision = '96d3e8caaf8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('unit_set', sa.Column('bounds', sa.String(length=256), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('unit_set', 'bounds')
    # ### end Alembic commands ###
