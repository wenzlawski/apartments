from app.api.deps import SessionDep
from app.models import (
    Settings,
    SettingsCreate,
    SettingsPublic,
)
from fastapi import APIRouter, Request
from sqlmodel import select

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/", response_model=SettingsPublic)
def read_settings(session: SessionDep, request: Request):
    settings = session.exec(select(Settings)).first()

    return settings


@router.put("/", response_model=SettingsPublic)
def update_settings(session: SessionDep, request: Request, settings_in: SettingsCreate):
    settings = session.exec(select(Settings)).first()

    # If it doesn't exist, create it using the new data (assuming `new_data` is a dict)
    if settings is None:
        settings = Settings.model_validate(settings_in)
        session.add(settings)
    else:
        # Update fields
        for key, value in settings_in.model_dump().items():
            setattr(settings, key, value)

    session.commit()
    session.refresh(settings)

    return settings
