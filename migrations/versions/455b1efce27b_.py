"""empty message

Revision ID: 455b1efce27b
Revises: 6e7a8a36e1ac
Create Date: 2023-11-12 18:47:26.884573

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '455b1efce27b'
down_revision = '6e7a8a36e1ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('paidStatus', sa.String(length=3), nullable=True))

    with op.batch_alter_table('transaction_item', schema=None) as batch_op:
        batch_op.drop_column('color')
        batch_op.drop_column('size')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('size', mysql.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('color', mysql.VARCHAR(length=100), nullable=True))

    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_column('paidStatus')

    # ### end Alembic commands ###