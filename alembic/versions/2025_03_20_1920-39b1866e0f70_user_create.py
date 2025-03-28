"""user_create

Revision ID: 39b1866e0f70
Revises: 
Create Date: 2025-03-20 19:20:51.770805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy  import FileType
from src.config import settings
from fastapi_storages import FileSystemStorage

# revision identifiers, used by Alembic.
revision: str = '39b1866e0f70'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
storage=FileSystemStorage(path=settings.BASE_DIR / "mediafiles" / "users" / "logo")

def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('logo', FileType(storage=storage), nullable=False),
    sa.Column('fullname', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
