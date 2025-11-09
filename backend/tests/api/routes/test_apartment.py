import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.apartment import create_random_apartment


def test_create_apartment(client: TestClient) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/apartments/",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content


def test_read_apartment(client: TestClient, db: Session) -> None:
    item = create_random_apartment(db)
    response = client.get(
        f"{settings.API_V1_STR}/apartments/{item.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
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


def test_read_apartments(client: TestClient, db: Session) -> None:
    create_random_apartment(db)
    create_random_apartment(db)
    response = client.get(
        f"{settings.API_V1_STR}/apartments/",
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_item(client: TestClient, db: Session) -> None:
    item = create_random_apartment(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/apartments/{item.id}",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["id"] == str(item.id)


def test_update_apartment_not_found(client: TestClient) -> None:
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/apartments/{uuid.uuid4()}",
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Apartment not found"


def test_delete_apartment(client: TestClient, db: Session) -> None:
    item = create_random_apartment(db)
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
