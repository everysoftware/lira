from dataclasses import dataclass
from typing import Literal, cast, Sequence, Self

from app.base.models import Entity
from app.base.schemas import BaseModel


@dataclass
class SortingEntry:
    field: str
    order: Literal["asc", "desc"] = "asc"

    @classmethod
    def from_str(cls, model_type: type[Entity], value: str) -> Self:
        values = value.lower().split(":")
        match len(values):
            case 1:
                field, order = values[0], "asc"
            case 2:
                field, order = values
            case _:
                raise ValueError(f"Invalid format: {value}")
        if order not in ["asc", "desc"]:
            raise ValueError(f"Invalid sorting order: {order}")
        if not hasattr(model_type, field):
            raise ValueError(f"Invalid sorting field: {field}")
        return cls(field, cast(Literal["asc", "desc"], order))


class Sorting(BaseModel):
    sort: str = "updated_at:desc"

    def render(self, model_type: type[Entity]) -> Sequence[SortingEntry]:
        sort = self.sort.split(",")
        return [SortingEntry.from_str(model_type, value) for value in sort]
