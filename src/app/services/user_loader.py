import httpx

from app.schemas import LoadResponse
from app.core import (
    r,
    settings,
)


async def load_users(limit: int) -> list[LoadResponse]:
    async with httpx.AsyncClient() as client:
        url = f"{settings.api_url}/api/?results={limit}"
        response = await client.get(url)

    users = response.json().get("results")

    if not users:
        return {}

    keys_to_delete = ("user:ids", "user:order")
    if await r.exists(*keys_to_delete):
        await r.delete(*keys_to_delete)

    pipe = r.pipeline()

    for user_id, user in enumerate(users, start=1):
        pipe.hset(
            f"user:{user_id}",
            mapping={
                "gender": user["gender"],
                "first_name": user["name"]["first"],
                "last_name": user["name"]["last"],
                "phone": user["phone"],
                "email": user["email"],
                "city": user["location"]["city"],
                "photo_url": user["picture"]["thumbnail"]
            }
        )
        pipe.sadd("user:ids", user_id)
        pipe.rpush("user:order", user_id)

    await pipe.execute()

    users_for_response = [
        {
            "gender": user["gender"],
            "first_name": user["name"]["first"],
            "last_name": user["name"]["last"],
            "phone": user["phone"],
            "email": user["email"],
            "city": user["location"]["city"],
            "photo_url": user["picture"]["thumbnail"]
        }
        for user in users
    ]

    return {"users": users_for_response}
