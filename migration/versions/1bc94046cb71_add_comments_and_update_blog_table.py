"""Add comments and update blog table

Revision ID: 1bc94046cb71
Revises: ea037ba5561a
Create Date: 2025-02-26 13:08:42.300068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bc94046cb71'
down_revision: Union[str, None] = 'ea037ba5561a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(length=200), nullable=False),
    sa.Column('date_publish', sa.DateTime(timezone=True), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('blog_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('blogs', sa.Column('status', sa.Enum('PUBLISH', 'HIDE', 'DELETE', name='blogstatus'), nullable=True))
    op.add_column('blogs', sa.Column('date_publish', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blogs', 'date_publish')
    op.drop_column('blogs', 'status')
    op.drop_table('comments')
    # ### end Alembic commands ###
