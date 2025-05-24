from typing import Any, Annotated

from fastapi import (
    APIRouter,
    status,
    Path,
)

from app.services.user_loader import load_users
from app.schemas.load import (
    LoadResponse, 
    LoadUsersRequest,
)
from app.services import get_paginated_users
from app.const import GE_USER_ID, LE_USER_ID



Limit = Annotated[
    int,
    Path(
        ...,
        title="User ID",
        ge=GE_USER_ID,
        le=LE_USER_ID,
    )
]


router = APIRouter()


@router.get(
    "/{page}",
    summary="Получение пользователей с пагинацией",
    description="Возвращает 5 пользователей на странице. Использует Redis.",
    status_code=status.HTTP_200_OK,
)
async def get_users_page(page: int) -> dict[str, Any]:
    return await get_paginated_users(page)


@router.post(
    "/load",
    response_model=LoadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Загрузить 1000 пользователей",
    description="Запрашивает 1000 пользователей с randomuser.me и сохраняет их в Redis",
)
async def load_users_endpoint(data: LoadUsersRequest) -> list[LoadResponse]:
    return await load_users(limit = data.limit)
