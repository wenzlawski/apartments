from faker import Faker
from sqlmodel import Session

from app import crud
from app.models import Apartment
from app.utils import generate_random_apartment

fake = Faker()


def create_random_apartment(db: Session) -> Apartment:
    item_in = generate_random_apartment()
    return crud.create_apartment(session=db, apartment_in=item_in)
