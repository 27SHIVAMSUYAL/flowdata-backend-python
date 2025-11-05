from pydantic import BaseModel, Field
from datetime import datetime , UTC


def _now_ts() -> int:
    return int(datetime.now(UTC).timestamp())


class Student(BaseModel):
    id: int
    name: str
    age: int
    roll_no: int
    grade: str
    created_at: int = Field(default_factory=_now_ts)
    updated_at: int = Field(default_factory=_now_ts)

