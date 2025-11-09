import logging

from faker import Faker
from sqlmodel import Session

from app.core.db import engine, init_db
from app.models import Apartment

logger = logging.getLogger(__name__)
fake = Faker()


def create_fake_apartments(session: Session, n=10):
    fake = Faker()
    for _ in range(n):
        apt = Apartment(
            title=fake.address()[:255],
            description=fake.text(max_nb_chars=100),
            rating=fake.random_int(1, 5),
        )
        session.add(apt)
    session.commit()
    session.close()


"""
Add fake data to the database
"""


def fake_init_db(session: Session) -> None:
    create_fake_apartments(session)


def init() -> None:
    with Session(engine) as session:
        init_db(session)
        fake_init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
