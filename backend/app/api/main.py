from fastapi import APIRouter

from app.api.routes import apartments, home, private, settings
from app.core.config import settings as set

api_router = APIRouter()

api_router.include_router(home.router)
api_router.include_router(apartments.router)
api_router.include_router(settings.router)

if set.ENVIRONMENT == "local":
    api_router.include_router(private.router)
