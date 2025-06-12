import redis.asyncio as aioredis


class CacheService:
    def __init__(self):
        self.client = None

    async def init(self):
        self.client = await aioredis.from_url(
            "redis://redis:6379",
            encoding="utf-8",
            decode_responses=True
        )

    async def get(self, key: str):
        return await self.client.get(key)

    async def set(self, key: str, value):
        await self.client.set(key, value)
