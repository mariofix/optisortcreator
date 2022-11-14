"""User.username

Revision ID: 0ba8ef35a0b5
Revises: 12b8b02663d6
Create Date: 2022-11-13 20:44:41.310040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0ba8ef35a0b5"
down_revision = "12b8b02663d6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("username", sa.String(length=255), nullable=True))
        batch_op.drop_constraint("uq_user_login", type_="unique")
        batch_op.create_unique_constraint(batch_op.f("uq_user_username"), ["username"])
        batch_op.drop_column("login")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("login", sa.VARCHAR(length=255), nullable=True))
        batch_op.drop_constraint(batch_op.f("uq_user_username"), type_="unique")
        batch_op.create_unique_constraint("uq_user_login", ["login"])
        batch_op.drop_column("username")

    # ### end Alembic commands ###