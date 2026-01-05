from app import crud
from app.models import Apartment
from app.utils import generate_random_apartment
from faker import Faker
from sqlmodel import Session


def create_random_apartment(db: Session, f: Faker) -> Apartment:
    item_in = generate_random_apartment(f)
    return crud.create_apartment(session=db, apartment_in=item_in)
