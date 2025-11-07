import uuid

from fastapi import Form
from sqlmodel import Field, SQLModel


# Shared properties
class ApartmentBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    rating: int | None = None


# Properties to receive on item creation
class ApartmentCreate(ApartmentBase):
    @classmethod
    def as_form(
        cls,
        title: str = Form(..., min_length=1, max_length=255),
        description: str | None = Form(None, max_length=255),
        rating: int | None = Form(None),
    ):
        return cls(title=title, description=description, rating=rating)


# Properties to receive on item update
class ApartmentUpdate(ApartmentBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    @classmethod
    def as_form(
        cls,
        title: str = Form(..., min_length=1, max_length=255),
        description: str | None = Form(None, max_length=255),
        rating: int | None = Form(None),
    ):
        return cls(title=title, description=description, rating=rating)



# Database model, database table inferred from class name
class Apartment(ApartmentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


# Properties to return via API, id is always required
class ApartmentPublic(ApartmentBase):
    id: uuid.UUID


class ApartmentsPublic(SQLModel):
    data: list[ApartmentPublic]
    count: int

# Generic message
class Message(SQLModel):
    message: str

# Shared properties
class SettingsBase(SQLModel):
    email: str | None = Field(default=None, min_length=1, max_length=255)
    cron_schedule: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class SettingsCreate(SettingsBase):
    @classmethod
    def as_form(
        cls,
        email: str = Form(..., min_length=1, max_length=255),
        cron_schedule: str | None = Form(None, max_length=255),
    ):
        return cls(email=email, cron_schedule=cron_schedule)


# Properties to receive on item update
class SettingsUpdate(SettingsBase):
    pass


# Database model, database table inferred from class name
class Settings(SettingsBase, table=True):
    id: int = Field(default=None, primary_key=True)


# Properties to return via API, id is always required
class SettingsPublic(SettingsBase):
    id: int
