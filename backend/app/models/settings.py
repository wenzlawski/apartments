from typing import Annotated

from pydantic import AfterValidator, EmailStr
from sqlmodel import Field, SQLModel

from app.models.utils import is_cron_string


# Shared properties
class SettingsBase(SQLModel):
    email: EmailStr | None = Field(default=None, min_length=1, max_length=255)
    cron_schedule: Annotated[str, AfterValidator(is_cron_string)] | None = Field(
        default=None, max_length=255
    )


# Properties to receive on item creation
class SettingsCreate(SettingsBase):
    pass


# Properties to receive on item update
class SettingsUpdate(SettingsBase):
    pass


# Database model, database table inferred from class name
class Settings(SettingsBase, table=True):
    id: int = Field(default=None, primary_key=True)


# Properties to return via API, id is always required
class SettingsPublic(SettingsBase):
    pass
