import logging

from sqlmodel import Session

from app.core.db import engine, init_db

logger = logging.getLogger(__name__)


def recompute_apartments(session: Session) -> None:
    # For each entry get the source html and parse it. Then alter the rows in bulk
    pass


def init() -> None:
    with Session(engine) as session:
        init_db(session)
        recompute_apartments(session)


def main() -> None:
    logger.info("Recomputing apartments from source.")
    init()
    logger.info("Finished recomputing apartments.")


if __name__ == "__main__":
    main()
