"""empty message

Revision ID: 791cd7d80402
Revises: 
Create Date: 2017-05-02 16:01:24.803337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '791cd7d80402'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipes',
    sa.Column('recipeid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('recipeid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipes')
    # ### end Alembic commands ###
