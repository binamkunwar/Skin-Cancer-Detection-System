"""migrationn

Revision ID: 37a37df20b4d
Revises: e79f94aa2cdf
Create Date: 2023-11-27 12:13:40.221065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37a37df20b4d'
down_revision = 'e79f94aa2cdf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Title', sa.String(length=100), nullable=True),
    sa.Column('Blog', sa.String(length=100), nullable=True),
    sa.Column('Writer', sa.Text(), nullable=True),
    sa.Column('phoneNumber', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog')
    # ### end Alembic commands ###
