import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from src.core.validators import validate_email
from src.database import Base, TimestampMixin

if TYPE_CHECKING:
    from src.users.models import User


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
    
    # Many-to-Many with Association Object
    users: Mapped[list["User"]] = relationship(secondary="career_page_user", back_populates="career_pages", viewonly=True)
    career_page_users: Mapped[list["CareerPageUser"]] = relationship(back_populates="career_page")

    @validates("contact_email")
    def validate_contact_email(self, key, address):
        return validate_email(address)

    def __str__(self) -> str:
        return f"CareerPage(id={self.id!s}, name={self.name}, currency={self.currency}, contact_email={self.contact_email})"


class CareerPageUser(TimestampMixin, Base):
    __tablename__ = "career_page_user"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    career_page_id: Mapped[UUID] = mapped_column(ForeignKey("career_page.id"), primary_key=True)
    status: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    last_active_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="career_page_users")
    career_page: Mapped["CareerPage"] = relationship(back_populates="career_page_users")
