from collections.abc import Generator

import pytest
from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.models import Apartment
from fastapi.testclient import TestClient
from sqlmodel import Session, delete


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session]:
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(Apartment)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return [settings.FAKER_LOCALE]


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return settings.FAKER_TEST_RANDOM_SEED
