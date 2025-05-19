from pydantic import BaseModel


class LoadResponse(BaseModel):

    status: str
    loaded: int
