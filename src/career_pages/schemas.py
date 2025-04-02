from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr


class CareerPageBase(BaseModel):
    name: str
    logo_url: str | None = None
    favicon_url: str | None = None
    social_media_url: str | None = None
    language_code: str
    is_referral_program: bool = False
    is_display_organization: bool = False
    is_powered_by_manatal: bool = False
    currency: str
    contact_email: EmailStr
    contact_phone: str
    contact_website: str
    is_share_job_social_media: bool = False


class CareerPageCreate(CareerPageBase):
    pass


class CareerPageUpdate(CareerPageBase):
    name: str | None = None
    language_code: str | None = None
    is_referral_program: bool | None = None
    is_display_organization: bool | None = None
    is_powered_by_manatal: bool | None = None
    currency: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    contact_website: str | None = None
    is_share_job_social_media: bool | None = None


class CareerPageRetrieve(CareerPageBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
