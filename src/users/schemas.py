from pydantic import UUID4, BaseModel, HttpUrl


class UserData(BaseModel):
    id: UUID4
    name: str
    logo: HttpUrl | str

