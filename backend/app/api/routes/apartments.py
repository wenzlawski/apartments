import logging
import uuid

from fastapi import APIRouter, Query, Request, Response
from fastapi.exceptions import HTTPException
from sqlmodel import func, select

from app import crud
from app.api.deps import SessionDep
from app.models import (
    Apartment,
    ApartmentCreate,
    ApartmentPublic,
    ApartmentsPublic,
    ApartmentUpdate,
    Message,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/apartments", tags=["apartments"])


# Dummy datastore
@router.get("/", response_model=ApartmentsPublic)
def read_items(
    session: SessionDep,
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    statement = select(Apartment).offset(skip).limit(limit)
    items = session.exec(statement).all()
    total = session.exec(select(func.count()).select_from(Apartment)).one()

    return ApartmentsPublic(data=items, count=total)


@router.get("/{id}", response_model=ApartmentPublic)
def get_apartment(request: Request, session: SessionDep, id: uuid.UUID):
    item = session.get(Apartment, id)
    if not item:
        raise HTTPException(status_code=404, detail="Apartment not found")

    return item


@router.post("/", response_model=ApartmentPublic)
def create_apartment(
    request: Request, session: SessionDep, apartment_in: ApartmentCreate
):
    db_apartment = crud.create_apartment(session=session, apartment_in=apartment_in)
    return db_apartment


@router.put("/{id}", response_model=ApartmentPublic)
@router.patch("/{id}", response_model=ApartmentPublic)
def put_apartment(
    id: uuid.UUID,
    session: SessionDep,
    apartment_in: ApartmentUpdate,
):
    apartment = session.get(Apartment, id)
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")

    update_dict = apartment_in.model_dump(exclude_unset=True)
    apartment.sqlmodel_update(update_dict)

    session.add(apartment)
    session.commit()
    session.refresh(apartment)
    return apartment


@router.delete("/{id}")
def delete_item(session: SessionDep, response: Response, id: uuid.UUID) -> Message:
    """
    Delete an item.
    """
    apartment = session.get(Apartment, id)
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")

    session.delete(apartment)
    session.commit()

    return Message(message="Apartment deleted successfully")
