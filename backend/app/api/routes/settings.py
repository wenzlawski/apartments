import logging

from app.api.deps import SessionDep
from app.models import (
    Settings,
    SettingsCreate,
    SettingsPublic,
)
from fastapi import APIRouter, Request
from sqlmodel import select

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/", response_model=SettingsPublic)
def read_settings(session: SessionDep, request: Request):
    settings = session.exec(select(Settings)).first()

    logger.info(f"{settings=}")

    return settings


@router.put("/", response_model=SettingsPublic)
@router.patch("/", response_model=SettingsPublic)
def upsert_settings(session: SessionDep, request: Request, settings_in: SettingsCreate):
    settings = session.get(Settings, 1)
    if settings is None:
        settings = Settings(id=1)

    # copy provided fields onto the model
    data = settings_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(settings, key, value)

    session.add(settings)
    session.commit()
    session.refresh(settings)
    return settings
