"""empty message

Revision ID: 3add3e2f940a
Revises: 360dfa577dda
Create Date: 2019-05-21 08:19:04.679979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3add3e2f940a"
down_revision = "360dfa577dda"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "districting_problem",
        sa.Column(
            "type", sa.String(length=256), nullable=False, server_default="districts"
        ),
    )
    op.alter_column("districting_problem", "type", server_default=None)
    op.alter_column(
        "districting_problem",
        "number_of_parts",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.add_column("place", sa.Column("landmarks", sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("place", "landmarks")
    op.alter_column(
        "districting_problem",
        "number_of_parts",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.drop_column("districting_problem", "type")
    # ### end Alembic commands ###
