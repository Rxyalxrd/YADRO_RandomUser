import httpx

from app.core import (
    get_redis,
    settings,
)


async def load_users():
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.api_url)
        users = response.json()["results"]

    r = await get_redis()

    keys_to_delete = ("user:ids", "user:order")
    if await r.exists(*keys_to_delete):
        await r.delete(*keys_to_delete)

    pipe = r.pipeline()

    for user_id, user in enumerate(users, start=1):
        pipe.hset(f"user:{user_id}", mapping={
            "gender": user["gender"],
            "first_name": user["name"]["first"],
            "last_name": user["name"]["last"],
            "phone": user["phone"],
            "email": user["email"],
            "city": user["location"]["city"],
            "photo_url": user["picture"]["thumbnail"]
        })
        pipe.sadd("user:ids", user_id)
        pipe.rpush("user:order", user_id)

    await pipe.execute()

    return {"status": "ok", "loaded": len(users)}
