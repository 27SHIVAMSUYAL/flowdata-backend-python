from pydantic import BaseModel, Field
from datetime import datetime , UTC


def _now_ts() -> int:
    return int(datetime.now(UTC).timestamp())


class Admin(BaseModel):
    username: str
    password: str
    email: str
    role: str = "admin"
    created: int = Field(default_factory=_now_ts)
    updated: int = Field(default_factory=_now_ts)


class Auth(BaseModel):
    username: str
    password: str