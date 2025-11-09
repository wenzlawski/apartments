from faker import Faker
from sqlmodel import Session

from app import crud
from app.models import Apartment, ApartmentCreate

fake = Faker()


def create_random_apartment(db: Session) -> Apartment:
    title = fake.name()
    description = fake.text()
    item_in = ApartmentCreate(title=title, description=description)
    return crud.create_apartment(session=db, apartment_in=item_in)
