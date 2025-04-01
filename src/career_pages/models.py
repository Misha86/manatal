import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.core.validators import validate_email
from src.database import Base, TimestampMixin


class CareerPage(TimestampMixin, Base):
    __tablename__ = "career_page"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(600))
    logo_url: Mapped[str | None] = mapped_column(String, nullable=True)
    favicon_url: Mapped[str | None] = mapped_column(String, nullable=True)
    social_media_url: Mapped[str | None] = mapped_column(String, nullable=True)
    langue_code: Mapped[str] = mapped_column(String)
    is_referral_program: Mapped[bool] = mapped_column(Boolean, default=False)
    is_display_organization: Mapped[bool] = mapped_column(Boolean, default=False)
    is_powered_by_manatal: Mapped[bool] = mapped_column(Boolean, default=False)
    currency: Mapped[str] = mapped_column(String)
    contact_email: Mapped[str] = mapped_column(String)
    contact_phone: Mapped[str] = mapped_column(String)
    contact_website: Mapped[str] = mapped_column(String)
    is_share_job_social_media: Mapped[bool] = mapped_column(Boolean, default=False)

    @validates("contact_email")
    def validate_contact_email(self, key, address):
        return validate_email(address)

    def __str__(self) -> str:
        return f"CareerPage(id={self.id!s}, name={self.name}, currency={self.currency}, contact_email={self.contact_email})"
