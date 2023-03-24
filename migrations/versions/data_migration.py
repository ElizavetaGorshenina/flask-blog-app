from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from blog.security import flask_bcrypt

# revision identifiers, used by Alembic.
revision = 'data_migration'
down_revision = '5a3d69ed58a0'
branch_labels = None
depends_on = None


def upgrade():
    user_table = table('user',
                       column('id', sa.Integer()),
                       column('username', sa.String(length=80)),
                       column('first_name', sa.String(length=120)),
                       column('last_name', sa.String(length=120)),
                       column('email', sa.String(length=255)),
                       column('is_staff', sa.Boolean()),
                       column('_password', sa.LargeBinary()),
                       )

    op.bulk_insert(user_table, [
        {"id": 1, "username": "admin", "first_name": "Mikhail", "last_name": "Kruglov", "email": "admin@blog.ru",
         "is_staff": True, "_password": flask_bcrypt.generate_password_hash("adminpass")}])


def downgrade():
    pass
