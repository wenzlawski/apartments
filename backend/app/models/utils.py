import re
from copy import deepcopy
from typing import Any

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

CRON_RE = re.compile(
    r"^((((\d+,)+\d+|(\d+(\/|-|#)\d+)|\d+L?|\*(\/\d+)?|L(-\d+)?|\?|[A-Z]{3}(-[A-Z]{3})?) ?){5,7})$"
)


def partial_model(model: type[BaseModel]):
    def make_field_optional(
        field: FieldInfo, default: Any = None
    ) -> tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = field.annotation | None  # Optional[field.annotation]
        return new.annotation, new

    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        },
    )


def is_cron_string(cron):
    if CRON_RE.fullmatch(cron):
        return cron
    raise ValueError(f"Invalid cron expression: {cron!r}")
