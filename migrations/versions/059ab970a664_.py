"""empty message

Revision ID: 059ab970a664
Revises: 9adf47765ef3
Create Date: 2023-11-29 20:59:09.588529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '059ab970a664'
down_revision = '9adf47765ef3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faq',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('faq')
    # ### end Alembic commands ###