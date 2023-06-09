"""initial migrations

Revision ID: 4051fc09178b
Revises: 
Create Date: 2023-04-08 12:20:32.315634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4051fc09178b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('admin_name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('mobile', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('admin_id'),
    sa.UniqueConstraint('admin_name'),
    sa.UniqueConstraint('email')
    )
    op.create_table('search_show',
    sa.Column('rowid', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('rowid')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('mobile', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('venue',
    sa.Column('venue_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('place', sa.String(), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('venue_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('show',
    sa.Column('show_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('ticket_price', sa.Float(), nullable=False),
    sa.Column('start_time', sa.String(), nullable=False),
    sa.Column('end_time', sa.String(), nullable=False),
    sa.Column('fill_count', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.venue_id'], ),
    sa.PrimaryKeyConstraint('show_id')
    )
    op.create_table('bookings',
    sa.Column('bid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('venue_name', sa.Integer(), nullable=False),
    sa.Column('show_id', sa.Integer(), nullable=False),
    sa.Column('show_title', sa.Integer(), nullable=False),
    sa.Column('num_seats', sa.Integer(), nullable=False),
    sa.Column('user_rating', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['show_id'], ['show.show_id'], ),
    sa.ForeignKeyConstraint(['show_title'], ['show.title'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.venue_id'], ),
    sa.ForeignKeyConstraint(['venue_name'], ['venue.name'], ),
    sa.PrimaryKeyConstraint('bid')
    )
    op.create_table('running',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('show_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.String(), nullable=False),
    sa.Column('end_time', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['show_id'], ['show.show_id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.venue_id'], ),
    sa.PrimaryKeyConstraint('venue_id', 'show_id')
    )
    op.create_table('tags',
    sa.Column('show_id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['show_id'], ['show.show_id'], ),
    sa.PrimaryKeyConstraint('show_id', 'tag')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.drop_table('running')
    op.drop_table('bookings')
    op.drop_table('show')
    op.drop_table('venue')
    op.drop_table('user')
    op.drop_table('search_show')
    op.drop_table('admin')
    # ### end Alembic commands ###
