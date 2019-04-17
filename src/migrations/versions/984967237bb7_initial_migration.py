"""
Initial migration.

Revision ID: 984967237bb7
Create Date: 2019-04-17 16:31:01.700088
"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '984967237bb7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=60), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('modified', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'stow',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('key', sa.String(length=100), nullable=True),
        sa.Column('value', sa.UnicodeText(), nullable=True),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('modified', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'key')
    )


def downgrade():
    op.drop_table('stow')
    op.drop_table('user')
