from pydantic import BaseModel


class UserResponse(BaseModel):

    gender: str
    first_name: str
    last_name: str
    phone: str
    email: str
    city: str
    photo_url: str
