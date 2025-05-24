import redis.asyncio as redis

from .settings import settings


redis = redis.Redis.from_url(
    settings.redis_url,
    decode_responses=True,
    encoding="utf-8",
)

