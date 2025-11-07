import uuid

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import func, select
from starlette.responses import JSONResponse, RedirectResponse

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
from app.utils import templates

router = APIRouter(prefix="/apartments")

# Dummy datastore
@router.get("/", response_model=ApartmentsPublic)
def read_items(session: SessionDep, request: Request):

    statement = select(Apartment)
    items = session.exec(statement).all()

    return ApartmentsPublic(data=items, count=len(items))


@router.get("/{id}", response_model=ApartmentPublic)
def get_apartment(request: Request, session: SessionDep, id: uuid.UUID):
    item = session.get(Apartment, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item

@router.post("/", response_model=ApartmentPublic)
def create_apartment(request: Request, session: SessionDep, apartment_in: ApartmentCreate):
    db_apartment = crud.create_apartment(session=session, apartment_in=apartment_in)
    return db_apartment


@router.put("/{id}", response_model=ApartmentPublic)
def update_apartment(
    id: uuid.UUID,
    session: SessionDep,
    apartment_in: ApartmentUpdate,
):
    apartment = session.get(Apartment, id)
    if not apartment:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = apartment_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(apartment, key, value)
    session.add(apartment)
    session.commit()
    session.refresh(apartment)
    return apartment


@router.delete("/{id}")
def delete_item(
        session: SessionDep, response: Response, id: uuid.UUID
) -> Message:
    """
    Delete an item.
    """
    apartment = session.get(Apartment, id)
    if not apartment:
        raise HTTPException(status_code=404, detail="Item not found")

    session.delete(apartment)
    session.commit()

    return Message(message="Apartment deleted successfully.")
