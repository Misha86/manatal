from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.core.validators import validate_email
from src.database import Base, TimestampMixin, UUIDMixin


class User(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "user"

    full_name: Mapped[str] = mapped_column(String(300))
    email: Mapped[str] = mapped_column(String(255))
    external_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), unique=True)

    @validates("email")
    def validate_email(self, key: str, address: str) -> str:
        return validate_email(address)

    def __str__(self) -> str:
        return f"User(id={self.id!s}, full_name={self.full_name}, email={self.email}, external_id={self.external_id!s})"
