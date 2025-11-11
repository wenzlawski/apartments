import uuid
from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel

from app.models.utils import partial_model


# Shared properties
class ApartmentBase(SQLModel):
    description: str | None = Field(default=None)
    rating: int | None = None
    num_rooms: Decimal = Field(max_digits=2, decimal_places=1)
    address: str = Field(min_length=1, max_length=512)
    posted_at: datetime
    area_sqm: Decimal = Field(max_digits=6, decimal_places=1)
    construction_year: int | None
    num_bathrooms: int
    floor: int
    maintenance_fee: Decimal = Field(max_digits=6, decimal_places=2)
    has_commission: bool | None
    posting_id: int
    seller_object_id: str
    price: Decimal = Field(max_digits=10, decimal_places=2)
    # TODO: Energy, available from, zustand, bodenbelag,
    # TODO: Computed field: ppm2 (area / price), coordinates (address), near amenities, obj properties (from pictures/description)
    # Should make all the computed things a json object


# Properties to receive on item creation
class ApartmentCreate(ApartmentBase):
    pass


@partial_model
class ApartmentUpdate(ApartmentBase):
    pass


# Database model, database table inferred from class name
class Apartment(ApartmentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


# Properties to return via API, id is always required
class ApartmentPublic(ApartmentBase):
    id: uuid.UUID


class ApartmentsPublic(SQLModel):
    data: list[ApartmentPublic]
    count: int
