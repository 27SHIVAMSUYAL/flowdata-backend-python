from pydantic import BaseModel, Field
from datetime import datetime , UTC


def _now_ts() -> int:
    return int(datetime.now(UTC).timestamp())


class User(BaseModel):
    username: str
    password: str
    email: str
    role: str = "user"
    created: int = Field(default_factory=_now_ts)
    updated: int = Field(default_factory=_now_ts)


class UserAuth(BaseModel):
    username: str
    password: str