import logging
from pathlib import Path

from fastapi.templating import Jinja2Templates

from app.core.config import settings

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def setup_logging() -> None:
    """Configure global logging for the application."""
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Optional: silence noisy loggers (e.g., from dependencies)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
