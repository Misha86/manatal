from sqlalchemy import JSON, Boolean, Column, Enum, ForeignKey, Integer, Numeric, String, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from src.career_pages.constants import Currency, UserCareerPageStatus
from src.core.validators import validate_email
from src.database import Base, TimestampMixin, UUIDMixin

job_post_link = Table(
    "job_post_link",
    Base.metadata,
    Column("job_post_id", ForeignKey("job_post.id"), primary_key=True),
    Column("external_job_post_id", ForeignKey("external_job_post.id"), primary_key=True),
)


class UserBase(TimestampMixin, UUIDMixin, Base):
    __abstract__ = True

    full_name: Mapped[str] = mapped_column(String(300))
    email: Mapped[str] = mapped_column(String(255))
    external_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), unique=True)

    @validates("email")
    def validate_email(self, key: str, address: str) -> str:
        return validate_email(address)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!s}, external_id={self.external_id!s})"


class User(UserBase):
    __tablename__ = "user"


class CareerPage(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "career_page"

    name: Mapped[str] = mapped_column(String(600))
    client_id: Mapped[str] = mapped_column(String)
    job_post_limit: Mapped[int] = mapped_column(Integer)
    logo_url: Mapped[str | None] = mapped_column(String, nullable=True)
    favicon_url: Mapped[str | None] = mapped_column(String, nullable=True)
    social_media_url: Mapped[str | None] = mapped_column(String, nullable=True)
    language_code: Mapped[str] = mapped_column(String)
    is_referral_program: Mapped[bool] = mapped_column(Boolean, default=False)
    is_display_organization: Mapped[bool] = mapped_column(Boolean, default=False)
    is_powered_by_manatal: Mapped[bool] = mapped_column(Boolean, default=False)
    currency: Mapped[str] = mapped_column(Enum(Currency, name="career_page_currency"), default=Currency.USD)
    contact_email: Mapped[str] = mapped_column(String(255))
    contact_phone: Mapped[str] = mapped_column(String)
    contact_website: Mapped[str] = mapped_column(String)
    is_share_job_social_media: Mapped[bool] = mapped_column(Boolean, default=False)

    users: Mapped[list["CareerPageUser"]] = relationship()
    social_medias: Mapped[list["SocialMedia"]] = relationship(back_populates="career_page")
    job_posts: Mapped[list["JobPost"]] = relationship(back_populates="career_page")
    application_forms: Mapped[list["ApplicationForm"]] = relationship(back_populates="career_page")

    @validates("contact_email")
    def validate_contact_email(self, key: str, address: str) -> str:
        return validate_email(address)

    def __str__(self) -> str:
        return f"CareerPage(id={self.id!s}, name={self.name}, currency={self.currency}, contact_email={self.contact_email})"


class CareerPageUser(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "career_page_user"

    status: Mapped[str] = mapped_column(
        Enum(UserCareerPageStatus, name="career_page_user_status"), default=UserCareerPageStatus.blocked
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    career_page_id: Mapped[UUID] = mapped_column(ForeignKey("career_page.id"))

    user: Mapped["User"] = relationship()


class SocialMedia(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "social_media"

    __table_args__ = (UniqueConstraint("career_page_id", "type", name="uix_career_page_type"),)

    type: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    career_page_id: Mapped[UUID] = mapped_column(ForeignKey("career_page.id"))
    career_page: Mapped["CareerPage"] = relationship(back_populates="social_medias")

    def __str__(self) -> str:
        return f"SocialMedia(id={self.id!s}, type={self.type}, url={self.url}, is_active={self.is_active})"


class Applicant(UserBase):
    __tablename__ = "applicant"


class Application(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "application"

    form: Mapped[dict] = mapped_column(JSON)

    applicant_id: Mapped[UUID] = mapped_column(ForeignKey("applicant.id"))
    job_post_id: Mapped[UUID] = mapped_column(ForeignKey("job_post.id"))
    applicant: Mapped["Applicant"] = relationship()


class ExternalJobPost(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "external_job_post"

    external_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), unique=True)

    job_posts: Mapped[list["JobPost"]] = relationship(secondary=job_post_link, back_populates="external_job_posts")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!s}, external_id={self.external_id}"


class JobPost(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "job_post"

    name: Mapped[str] = mapped_column(String(600))
    status: Mapped[str] = mapped_column(String)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_hide_salary: Mapped[bool] = mapped_column(Boolean, default=False)
    payment_frequency: Mapped[str] = mapped_column(String)
    work_type: Mapped[str] = mapped_column(String)
    headcount: Mapped[int] = mapped_column(Integer)
    header_key: Mapped[str] = mapped_column(String, nullable=True)
    minimum_salary: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    maximum_salary: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))

    applicants: Mapped[list["Application"]] = relationship()
    job_post_translations: Mapped[list["JobPosTranslation"]] = relationship(back_populates="job_post")

    application_form_id: Mapped[UUID] = mapped_column(ForeignKey("application_form.id"))
    application_form: Mapped["ApplicationForm"] = relationship(back_populates="job_posts")

    career_page_id: Mapped[UUID] = mapped_column(ForeignKey("career_page.id"))
    career_page: Mapped["CareerPage"] = relationship(back_populates="job_posts")

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship()

    external_job_posts: Mapped[list["ExternalJobPost"]] = relationship(secondary=job_post_link, back_populates="job_posts")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!s}, name={self.name}, status={self.status})"


class JobPosTranslation(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "job_post_translation"

    language_code: Mapped[str] = mapped_column(String)

    job_post_id: Mapped[UUID] = mapped_column(ForeignKey("job_post.id"))
    job_post: Mapped["JobPost"] = relationship(back_populates="job_post_translations")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!s}, language_code={self.language_code})"


class ApplicationForm(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "application_form"

    name: Mapped[str] = mapped_column(String(600))
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)

    career_page_id: Mapped[UUID] = mapped_column(ForeignKey("career_page.id"))
    career_page: Mapped["CareerPage"] = relationship(back_populates="application_forms")

    job_posts: Mapped[list["JobPost"]] = relationship(back_populates="application_form")
    application_form_fields: Mapped[list["ApplicationFormField"]] = relationship(back_populates="application_form")

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!s}, name={self.name}, is_default={self.is_default})"


class ApplicationFormField(TimestampMixin, UUIDMixin, Base):
    __tablename__ = "application_form_field"

    name: Mapped[str] = mapped_column(String(600))
    label: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)
    source: Mapped[str] = mapped_column(String)
    rank: Mapped[int] = mapped_column(Integer)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False)
    options: Mapped[dict] = mapped_column(JSON)

    application_form_id: Mapped[UUID] = mapped_column(ForeignKey("application_form.id"))
    application_form: Mapped["ApplicationForm"] = relationship(back_populates="application_form_fields")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!s}, name={self.name}, is_default={self.is_default})"
