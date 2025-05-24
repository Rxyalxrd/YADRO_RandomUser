import random
from typing import Annotated

from fastapi import (
    APIRouter,
    Path,
    status,
)
from fastapi.exceptions import HTTPException
from redis.exceptions import RedisError

from app.core import get_redis
from app.schemas import UserResponse
from app.const import (
    GE_USER_ID,
    LE_USER_ID,
    RDS_LEFT_RANGE,
    RDS_RIGHT_RANGE,
)


router = APIRouter()


UserID = Annotated[
    int,
    Path(
        ...,
        title="User ID",
        ge=GE_USER_ID,
        le=LE_USER_ID,
    )
]


@router.get(
    "/random",
    summary="Получить случайного пользователя",
    description="Возвращает информацию о случайно выбранном пользователе из загруженных данных",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_random_user() -> UserResponse:
    r = await get_redis()

    try:
        user_ids = await r.lrange(
            "user:order", RDS_LEFT_RANGE, RDS_RIGHT_RANGE
        )

        if not user_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователи не загружены",
            )

        random_id = random.choice(user_ids)
        user = await r.hgetall(f"user:{random_id}")

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        return user

    except RedisError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка сервера",
        )


@router.get(
    "/{user_id}",
    summary="Получить пользователя по ID",
    description="Возвращает информацию о пользователе по его ID",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_user_by_id(user_id: UserID) -> UserResponse:
    r = await get_redis()

    try:
        user = await r.hgetall(f"user:{user_id}")

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        return user

    except RedisError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка сервера",
        )
