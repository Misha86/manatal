import uuid
from typing import Optional

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.config import settings
from src.core.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    logo: Mapped[FileType] = mapped_column(
        FileType(storage=FileSystemStorage(path=settings.BASE_DIR / "mediafiles" / "users" / "logo"))
    )
    fullname: Mapped[Optional[str]]

    def __str__(self) -> str:
        return f"User(id={self.id!s}, name={self.name!s}, fullname={self.fullname!s})"
