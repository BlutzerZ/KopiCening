"""empty message

Revision ID: 6e7a8a36e1ac
Revises: 3cd1591a26e4
Create Date: 2023-11-12 03:36:42.601198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e7a8a36e1ac'
down_revision = '3cd1591a26e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('priceBase', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('priceBase')

    # ### end Alembic commands ###
