"""empty message

Revision ID: 92cdd9061ece
Revises: 
Create Date: 2020-10-30 13:47:56.804252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92cdd9061ece'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('bg_color', sa.String(length=50), nullable=True, default="orange"),)
    op.add_column('users', sa.Column('profile_pic', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_pic')
    op.drop_column('users', 'bg_color')
    # ### end Alembic commands ###
