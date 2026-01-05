import uuid
from datetime import datetime
from decimal import Decimal

from sqlmodel import Column, DateTime, Field, Numeric, Relationship, SQLModel, Text

from app.models.utils import partial_model


# Shared properties
class ApartmentBase(SQLModel):
    description: str | None = Field(default=None)
    rating: int | None = None
    num_rooms: Decimal = Field(default=None, sa_column=Column(Numeric(2, 1)))
    address: str | None = Field(default=None, sa_column=Column(Text))
    posted_at: datetime | None = None
    area_sqm: Decimal | None = Field(default=None, sa_column=Column(Numeric(6, 1)))
    construction_year: int | None = None
    num_bathrooms: int | None = None
    floor: int | None = None
    maintenance_fee: Decimal | None = Field(
        default=None, sa_column=Column(Numeric(6, 2))
    )
    has_commission: bool | None = None
    posting_id: str | None = None
    seller_object_id: str | None = None
    price: Decimal | None = Field(default=None, sa_column=Column(Numeric(10, 2)))


class ApartmentPageBase(SQLModel):
    url: str = Field(..., max_length=2048)
    content: str = Field(sa_column=Column(Text))
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

    inserted_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, default=datetime.utcnow),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
    )


# Properties to receive on item creation
class ApartmentCreate(ApartmentBase):
    pass


@partial_model
class ApartmentUpdate(ApartmentBase):
    pass


# Database model, database table inferred from class name
class Apartment(ApartmentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    pages: list["ApartmentPage"] | None = Relationship(back_populates="apartment")


class ApartmentPage(ApartmentPageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    apartment_id: uuid.UUID = Field(foreign_key="apartment.id")
    apartment: Apartment | None = Relationship(back_populates="pages")


# Properties to return via API, id is always required
class ApartmentPublic(ApartmentBase):
    id: uuid.UUID


class ApartmentsPublic(SQLModel):
    data: list[ApartmentPublic]
    count: int
