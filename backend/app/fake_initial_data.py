import logging

from sqlmodel import Session

from app.core.db import engine, init_db
from app.models import Apartment
from app.utils import generate_random_apartment

logger = logging.getLogger(__name__)


def create_fake_apartments(session: Session, n=10):
    for _ in range(n):
        apt = Apartment.model_validate(generate_random_apartment())
        session.add(apt)
    session.commit()
    session.close()


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
