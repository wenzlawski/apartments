import logging

import pytest
from app.core.config import settings
from faker import Faker
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

logger = logging.getLogger(__name__)


def test_read_settings_no_exist(client: TestClient, faker: Faker):
    response = client.get(f"{settings.API_V1_STR}/settings/")

    assert response.status_code == 200

    content = response.json()
    assert content["email"] is None
    assert content["cron_schedule"] is None
    assert content["id"] == 1


def test_put_settings_exist(client: TestClient, faker: Faker):
    data = {"email": "test@test.de", "cron_schedule": "* * * * *"}
    response = client.put(
        f"{settings.API_V1_STR}/settings/", json=jsonable_encoder(data)
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == 1
    assert content["email"] == "test@test.de"
    assert content["cron_schedule"] == "* * * * *"


def test_put_invalid_email(client: TestClient, faker: Faker):
    data = {
        "email": "testtest.de",
    }
    response = client.put(
        f"{settings.API_V1_STR}/settings/", json=jsonable_encoder(data)
    )
    assert response.status_code == 422


def test_put_invalid_cron(client: TestClient, faker: Faker):
    data = {
        "cron_schedule": "30 23 a * *",
    }
    response = client.put(
        f"{settings.API_V1_STR}/settings/", json=jsonable_encoder(data)
    )
    assert response.status_code == 422


@pytest.mark.parametrize(
    "cron",
    [
        "* * * * *",
        "30 23 * * *",
        "5 23 * * *",
        "5,20,35 7-11 1-10 1,3 1",
        "5,20,35 7-11,13-17 1-10,20-25 1,3,5,7,9,11 1,3,5",
    ],
)
def test_put_valid_crons(client: TestClient, faker: Faker, cron: str):
    data = {
        "cron_schedule": cron,
    }
    response = client.put(
        f"{settings.API_V1_STR}/settings/", json=jsonable_encoder(data)
    )
    assert response.status_code == 200
