from pydantic import BaseModel


class IgnoreUsersList(BaseModel):
    users: list[str]
