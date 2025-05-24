from pydantic import BaseModel
from .user import UserResponse


class LoadResponse(BaseModel):
    users: list[UserResponse]


class LoadUsersRequest(BaseModel):
    limit: int
