from typing import Any

from fastapi import (
    APIRouter,
    status,
)

from app.services.user_loader import load_users
from app.schemas.load import LoadResponse
from app.services import get_paginated_users


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
async def load_users_endpoint() -> LoadResponse:
    return await load_users()
