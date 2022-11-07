"""Add IconSet table

Revision ID: b744e19ee62c
Revises: 
Create Date: 2022-11-07 11:12:32.492509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b744e19ee62c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('author', 'fio',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('author', 'birthday',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('author', 'biography',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('book', 'name_book',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('book', 'year_book',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('book', 'id_language',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('book', 'id_author',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('book', 'state_read',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.drop_constraint('auth', 'book', type_='foreignkey')
    op.drop_constraint('lang', 'book', type_='foreignkey')
    op.create_foreign_key(None, 'book', 'language', ['id_language'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'book', 'author', ['id_author'], ['id'], ondelete='CASCADE')
    op.alter_column('language', 'language',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_constraint('auth', 'languages', type_='foreignkey')
    op.drop_constraint('lang', 'languages', type_='foreignkey')
    op.create_foreign_key(None, 'languages', 'author', ['id_author'], ['id'])
    op.create_foreign_key(None, 'languages', 'language', ['id_language'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'languages', type_='foreignkey')
    op.drop_constraint(None, 'languages', type_='foreignkey')
    op.create_foreign_key('lang', 'languages', 'language', ['id_language'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key('auth', 'languages', 'author', ['id_author'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.alter_column('language', 'language',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_constraint(None, 'book', type_='foreignkey')
    op.drop_constraint(None, 'book', type_='foreignkey')
    op.create_foreign_key('lang', 'book', 'language', ['id_language'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key('auth', 'book', 'author', ['id_author'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.alter_column('book', 'state_read',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    op.alter_column('book', 'id_author',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('book', 'id_language',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('book', 'year_book',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('book', 'name_book',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('author', 'biography',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('author', 'birthday',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('author', 'fio',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
