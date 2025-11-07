from sqlmodel import Session

from app.models import Apartment, ApartmentCreate


def create_apartment(*, session: Session, apartment_in: ApartmentCreate) -> Apartment:
    db_item = Apartment.model_validate(apartment_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
