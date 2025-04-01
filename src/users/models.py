import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.core.validators import validate_email
from src.database import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(300))
    email: Mapped[str] = mapped_column(String)
    external_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))

    @validates("email")
    def validate_email(self, key, address):
        return validate_email(address)

    def __str__(self) -> str:
        return f"User(id={self.id!s}, name={self.name!s}, fullname={self.fullname!s})"
