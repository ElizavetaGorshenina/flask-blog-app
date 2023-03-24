"""user model created

Revision ID: 5a3d69ed58a0
Revises: 
Create Date: 2023-03-05 00:38:17.943750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a3d69ed58a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('first_name', sa.String(length=120), server_default='', nullable=False),
    sa.Column('last_name', sa.String(length=120), server_default='', nullable=False),
    sa.Column('email', sa.String(length=255), server_default='', nullable=False),
    sa.Column('is_staff', sa.Boolean(), nullable=False),
    sa.Column('_password', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###