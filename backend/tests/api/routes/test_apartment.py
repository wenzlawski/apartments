import logging
import uuid

from app.core.config import settings
from app.utils import generate_random_apartment
from faker import Faker
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlmodel import Session
from tests.utils.apartment import create_random_apartment

logger = logging.getLogger(__name__)


def test_create_apartment(client: TestClient, faker: Faker) -> None:
    a = generate_random_apartment(faker)
    data = a.model_dump()
    response = client.post(
        f"{settings.API_V1_STR}/apartments/",
        json=jsonable_encoder(data),
    )
    assert response.status_code == 200
    content = response.json()
    assert content["description"] == data["description"]
    assert "id" in content


def test_read_apartment(client: TestClient, db: Session, faker: Faker) -> None:
    item = create_random_apartment(db, faker)
    response = client.get(
        f"{settings.API_V1_STR}/apartments/{item.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["description"] == item.description
    assert content["id"] == str(item.id)


def test_read_apartment_not_found(
    client: TestClient,
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/apartments/{uuid.uuid4()}",
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Apartment not found"


def test_read_apartments(client: TestClient, db: Session, faker: Faker) -> None:
    create_random_apartment(db, faker)
    create_random_apartment(db, faker)
    response = client.get(
        f"{settings.API_V1_STR}/apartments/",
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_put_apartment(client: TestClient, db: Session, faker: Faker) -> None:
    apartment = create_random_apartment(db, faker)
    a = generate_random_apartment(faker)
    data = a.model_dump()
    response = client.put(
        f"{settings.API_V1_STR}/apartments/{apartment.id}", json=jsonable_encoder(data)
    )
    assert response.status_code == 200
    content = response.json()
    assert content["description"] == data["description"]
    assert content["rating"] == data["rating"]
    assert content["id"] == str(apartment.id)


def test_put_apartment_not_found(client: TestClient, faker: Faker) -> None:
    a = generate_random_apartment(faker)
    data = a.model_dump()
    response = client.put(
        f"{settings.API_V1_STR}/apartments/{uuid.uuid4()}", json=jsonable_encoder(data)
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Apartment not found"


def test_patch_apartment(client: TestClient, db: Session, faker: Faker) -> None:
    apartment = create_random_apartment(db, faker)
    data = {"description": "Updated description"}
    response = client.patch(
        f"{settings.API_V1_STR}/apartments/{apartment.id}",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["description"] == data["description"]
    assert content["rating"] == int(apartment.rating)
    assert content["id"] == str(apartment.id)


def test_delete_apartment(client: TestClient, db: Session, faker: Faker) -> None:
    item = create_random_apartment(db, faker)
    response = client.delete(
        f"{settings.API_V1_STR}/apartments/{item.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Apartment deleted successfully"


def test_delete_apartment_not_found(client: TestClient) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/apartments/{uuid.uuid4()}",
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Apartment not found"
