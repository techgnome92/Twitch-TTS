from pydantic import BaseModel


class AllowedUser(BaseModel):
    username: str
    voice: str


class AllowedUsersList(BaseModel):
    users: list[AllowedUser | None]


class IgnoreUsersList(BaseModel):
    users: list[str]
