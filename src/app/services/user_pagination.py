from typing import Any

from app.core import get_redis
from app.const import PAGE_SIZE


async def get_paginated_users(page: int = 1) -> dict[str, Any]:
    r = await get_redis()

    total = await r.llen("user:order")
    page = max(1, page)
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE - 1

    user_ids: list[int] = await r.lrange("user:order", start, end)

    if not user_ids:
        return {
            "page": page,
            "per_page": PAGE_SIZE,
            "total": total,
            "users": []
        }

    pipe = r.pipeline()

    for uid in user_ids:
        pipe.hgetall(f"user:{uid}")

    users_data: list[dict[str, Any]] = await pipe.execute()

    return {
        "page": page,
        "per_page": PAGE_SIZE,
        "total": total,
        "users": users_data
    }