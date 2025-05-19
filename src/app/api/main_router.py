from fastapi import APIRouter

from .endpoints import (
    load_router,
    user_router,
)

main_router = APIRouter()

main_router.include_router(
    load_router,
    prefix="/users",
    tags=["Random"],
)
main_router.include_router(
    user_router,
    prefix="/hompage",
    tags=["Users"],
)