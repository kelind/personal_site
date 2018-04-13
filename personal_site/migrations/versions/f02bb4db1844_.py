"""empty message

Revision ID: f02bb4db1844
Revises: bc81e9ba0377
Create Date: 2017-04-10 08:54:27.783354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f02bb4db1844'
down_revision = 'bc81e9ba0377'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=254), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('mailing')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mailing',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('address', sa.VARCHAR(length=254), nullable=True),
    sa.Column('tag_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('email')
    # ### end Alembic commands ###
