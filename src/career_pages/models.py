from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from src.core.validators import validate_email
from src.database import Base, TimestampMixin, UUIDMixin
from src.users.models import User


class CareerPage(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "career_page"

    name: Mapped[str] = mapped_column(String(600))
    logo_url: Mapped[str | None] = mapped_column(String, nullable=True)
    favicon_url: Mapped[str | None] = mapped_column(String, nullable=True)
    social_media_url: Mapped[str | None] = mapped_column(String, nullable=True)
    langue_code: Mapped[str] = mapped_column(String)
    is_referral_program: Mapped[bool] = mapped_column(Boolean, default=False)
    is_display_organization: Mapped[bool] = mapped_column(Boolean, default=False)
    is_powered_by_manatal: Mapped[bool] = mapped_column(Boolean, default=False)
    currency: Mapped[str] = mapped_column(String)
    contact_email: Mapped[str] = mapped_column(String(255))
    contact_phone: Mapped[str] = mapped_column(String)
    contact_website: Mapped[str] = mapped_column(String)
    is_share_job_social_media: Mapped[bool] = mapped_column(Boolean, default=False)

    users: Mapped[list["CareerPageUser"]] = relationship()
    social_medias: Mapped[list["SocialMedia"]] = relationship(back_populates="career_page")


    @validates("contact_email")
    def validate_contact_email(self, key: str, address: str) -> str:
        return validate_email(address)

    def __str__(self) -> str:
        return f"CareerPage(id={self.id!s}, name={self.name}, currency={self.currency}, contact_email={self.contact_email})"


class CareerPageUser(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "career_page_user"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    career_page_id: Mapped[UUID] = mapped_column(ForeignKey("career_page.id"))
    status: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    last_active_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=func.now())

    user: Mapped["User"] = relationship()


class SocialMedia(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "social_media"

    career_page_id: Mapped[UUID] = mapped_column(ForeignKey("career_page.id"))
    career_page: Mapped["CareerPage"] = relationship(back_populates="social_medias")
    type: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    def __str__(self) -> str:
        return f"SocialMedia(id={self.id!s}, type={self.type}, url={self.url}, is_active={self.is_active})"