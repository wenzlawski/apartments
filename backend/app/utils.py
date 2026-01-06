import json
import logging
from decimal import Decimal
from pathlib import Path

from faker import Faker
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.models import ApartmentCreate

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


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


def generate_random_apartment(f: Faker) -> ApartmentCreate:
    return ApartmentCreate(
        description=f.text(max_nb_chars=100),
        rating=f.random_int(1, 5),
        num_rooms=f.random_int(1, 3),
        address=f.address(),
        posted_at=f.date_time_this_year(),
        area_sqm=f.pyfloat(max_value=150, min_value=50, positive=True, right_digits=1),
        construction_year=f.random_int(1850, 2000),
        num_bathrooms=f.random_int(1, 3),
        floor=f.random_int(0, 8),
        maintenance_fee=f.pyfloat(
            max_value=500, min_value=100, positive=True, right_digits=2
        ),
        has_commission=f.boolean(),
        posting_id=f.pystr(10),
        seller_object_id=f.pystr(min_chars=10, max_chars=20),
        price=f.pyfloat(
            max_value=1_000_000, min_value=100_000, positive=True, right_digits=2
        ),
    )
