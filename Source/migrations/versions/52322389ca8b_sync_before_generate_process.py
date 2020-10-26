"""sync before generate process

Revision ID: 52322389ca8b
Revises: cb9b2b139393
Create Date: 2020-10-21 10:11:13.556405

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '52322389ca8b'
down_revision = 'cb9b2b139393'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('runmission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mission_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('stage_id', sa.Integer(), nullable=True),
    sa.Column('site_version', sa.Text(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('mission', sa.Column('mission_type', sa.Integer(), nullable=True))
    op.add_column('site', sa.Column('auto_dir', sa.Text(), nullable=True))
    op.add_column('site', sa.Column('execrsice_conn', sa.Text(), nullable=True))
    op.add_column('site', sa.Column('execrsice_db', sa.Text(), nullable=True))
    op.add_column('site', sa.Column('ext_scenario_filer', sa.Text(), nullable=True))
    op.add_column('site', sa.Column('octopus_conn', sa.Text(), nullable=True))
    op.add_column('site', sa.Column('octopus_db', sa.Text(), nullable=True))
    op.add_column('site', sa.Column('recording_db', sa.Text(), nullable=True))
    op.add_column('site', sa.Column('site_conn', sa.Text(), nullable=True))
    op.drop_column('site', 'auto_data_site_ip')
    op.drop_column('site', 'execrsice_db_ip')
    op.drop_column('site', 'execrsice_site_ip')
    op.drop_column('site', 'recording_db_ip')
    op.drop_column('site', 'auto_data_db_ip')
    op.drop_column('site', 'site_ip')
    op.add_column('stagerunmani', sa.Column('changed_by', sa.Integer(), nullable=True))
    op.add_column('stagerunmani', sa.Column('project_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stagerunmani', 'project_id')
    op.drop_column('stagerunmani', 'changed_by')
    op.add_column('site', sa.Column('site_ip', mysql.TEXT(), nullable=True))
    op.add_column('site', sa.Column('auto_data_db_ip', mysql.TEXT(), nullable=True))
    op.add_column('site', sa.Column('recording_db_ip', mysql.TEXT(), nullable=True))
    op.add_column('site', sa.Column('execrsice_site_ip', mysql.TEXT(), nullable=True))
    op.add_column('site', sa.Column('execrsice_db_ip', mysql.TEXT(), nullable=True))
    op.add_column('site', sa.Column('auto_data_site_ip', mysql.TEXT(), nullable=True))
    op.drop_column('site', 'site_conn')
    op.drop_column('site', 'recording_db')
    op.drop_column('site', 'octopus_db')
    op.drop_column('site', 'octopus_conn')
    op.drop_column('site', 'ext_scenario_filer')
    op.drop_column('site', 'execrsice_db')
    op.drop_column('site', 'execrsice_conn')
    op.drop_column('site', 'auto_dir')
    op.drop_column('mission', 'mission_type')
    op.drop_table('runmission')
    # ### end Alembic commands ###
