import uuid

from sqlmodel import Field, SQLModel


# Shared properties
class ApartmentBase(SQLModel):
    title: str = Field(min_length=1, max_length=512)
    description: str | None = Field(default=None)
    rating: int | None = None
    # num_rooms: int
    # address: str = Field(min_length=1, max_length=512)
    # posted_at: datetime
    # area_sqm: float
    # construction_year: int
    # num_bathrooms: int
    # floor: int
    # maintenance_fee: float
    # has_commission: bool
    # posting_id: int
    # seller_object_id: str
    # price: float
    # TODO: Energy, available from, zustand, bodenbelag,
    # TODO: Computed field: ppm2 (area / price), coordinates (address), near amenities, obj properties (from pictures/description)
    # Should make all the computed things a json object


# Properties to receive on item creation
class ApartmentCreate(ApartmentBase):
    pass


# Properties to receive on item update
class ApartmentUpdate(ApartmentBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


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
