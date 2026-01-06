import logging
from collections.abc import Generator

import pytest
from alembic import command
from alembic.config import Config
from app.api.deps import get_db
from app.core.config import settings
from app.core.db import create_db_engine, init_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import Session

logger = logging.getLogger(__name__)

# engine = create_db_engine(str(settings.SQLALCHEMY_TEST_DATABASE_URI))


def run_migrations(url: str):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", url)
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    url = str(settings.SQLALCHEMY_TEST_DATABASE_URI)
    if database_exists(url):
        drop_database(url)
    create_database(url)

    run_migrations(url)
    yield
    # Optional: drop DB afterwards
    drop_database(url)


@pytest.fixture(scope="session")
def engine(setup_database):
    eng = create_db_engine(str(settings.SQLALCHEMY_TEST_DATABASE_URI))
    yield eng
    eng.dispose()  # close all connections explicitly


@pytest.fixture(scope="function")
def db(engine) -> Generator[Session]:
    with Session(engine) as session:
        init_db(session)
        yield session
        # statement = delete(ApartmentPage)
        # session.execute(statement)
        # statement = delete(Apartment)
        # session.execute(statement)
        # statement = delete(Settings)
        # session.execute(statement)
        # session.commit()


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return [settings.FAKER_LOCALE]


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return settings.FAKER_TEST_RANDOM_SEED
