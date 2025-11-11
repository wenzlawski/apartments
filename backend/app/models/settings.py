from sqlmodel import Field, SQLModel


# Shared properties
class SettingsBase(SQLModel):
    email: str | None = Field(default=None, min_length=1, max_length=255)
    cron_schedule: str | None = Field(default=None, max_length=255)


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
    id: int
