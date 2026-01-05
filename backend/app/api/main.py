from app.api.routes import apartments, home, private, settings, utils
from app.core.config import settings as set
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(home.router)
api_router.include_router(apartments.router)
api_router.include_router(settings.router)
api_router.include_router(utils.router)

if set.ENVIRONMENT == "local":
    api_router.include_router(private.router)
