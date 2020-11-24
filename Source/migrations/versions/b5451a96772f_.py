"""empty message

Revision ID: b5451a96772f
Revises: 6dc4325a123c
Create Date: 2020-11-22 21:24:32.301001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5451a96772f'
down_revision = '6dc4325a123c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('generatestage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('generate_status_id', sa.Integer(), nullable=True),
    sa.Column('succedded', sa.Integer(), nullable=True),
    sa.Column('failed', sa.Integer(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.Column('stage_type', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('generatestage')
    # ### end Alembic commands ###
