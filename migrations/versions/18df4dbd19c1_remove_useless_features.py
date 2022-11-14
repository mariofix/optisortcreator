"""Remove useless features

Revision ID: 18df4dbd19c1
Revises: 0ba8ef35a0b5
Create Date: 2022-11-13 22:57:39.435148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "18df4dbd19c1"
down_revision = "0ba8ef35a0b5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("role", schema=None) as batch_op:
        batch_op.alter_column("updated_at", existing_type=sa.DATETIME(), nullable=False)

    with op.batch_alter_table("svs_contact", schema=None) as batch_op:
        batch_op.alter_column("updated_at", existing_type=sa.DATETIME(), nullable=False)

    with op.batch_alter_table("svs_customer", schema=None) as batch_op:
        batch_op.alter_column("updated_at", existing_type=sa.DATETIME(), nullable=False)

    with op.batch_alter_table("svs_machine", schema=None) as batch_op:
        batch_op.alter_column("updated_at", existing_type=sa.DATETIME(), nullable=False)

    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column("updated_at", existing_type=sa.DATETIME(), nullable=False)
        batch_op.drop_column("login_count")
        batch_op.drop_column("last_login_ip")
        batch_op.drop_column("current_login_at")
        batch_op.drop_column("confirmed_at")
        batch_op.drop_column("last_login_at")
        batch_op.drop_column("current_login_ip")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("current_login_ip", sa.VARCHAR(length=100), nullable=True)
        )
        batch_op.add_column(sa.Column("last_login_at", sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column("confirmed_at", sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column("current_login_at", sa.DATETIME(), nullable=True))
        batch_op.add_column(
            sa.Column("last_login_ip", sa.VARCHAR(length=100), nullable=True)
        )
        batch_op.add_column(sa.Column("login_count", sa.INTEGER(), nullable=True))
        batch_op.alter_column("updated_at", existing_type=sa.DATETIME(), nullable=True)

    with op.batch_alter_table("svs_machine", schema=None) as batch_op:
        batch_op.alter_column("updated_at", existing_type=sa.DATETIME(), nullable=True)

    with op.batch_alter_table("svs_customer", schema=None) as batch_op:
        batch_op.alter_column("updated_at", existing_type=sa.DATETIME(), nullable=True)

    with op.batch_alter_table("svs_contact", schema=None) as batch_op:
        batch_op.alter_column("updated_at", existing_type=sa.DATETIME(), nullable=True)

    with op.batch_alter_table("role", schema=None) as batch_op:
        batch_op.alter_column("updated_at", existing_type=sa.DATETIME(), nullable=True)

    # ### end Alembic commands ###
