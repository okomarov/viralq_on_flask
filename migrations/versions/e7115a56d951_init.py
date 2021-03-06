"""Init

Revision ID: e7115a56d951
Revises: 
Create Date: 2019-10-29 12:32:55.025254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7115a56d951'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('email_confirmed', sa.Boolean(), nullable=True),
    sa.Column('email_confirmed_on', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('waitlist',
    sa.Column('uuid', sa.String(length=8), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('referral',
    sa.Column('referring', sa.String(length=8), nullable=False),
    sa.Column('referred', sa.String(length=8), nullable=False),
    sa.ForeignKeyConstraint(['referred'], ['waitlist.uuid'], ),
    sa.ForeignKeyConstraint(['referring'], ['waitlist.uuid'], ),
    sa.PrimaryKeyConstraint('referring', 'referred', name='referrals_pk')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('referral')
    op.drop_table('waitlist')
    op.drop_table('user')
    # ### end Alembic commands ###
