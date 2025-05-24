import redis.asyncio as redis

from .setting import settings

async def get_redis() -> redis.Redis:
    return redis.Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        encoding="utf-8",
    )

