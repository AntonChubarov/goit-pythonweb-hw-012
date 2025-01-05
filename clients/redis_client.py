import os

import aioredis

from services.auth_service import ICache

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379")


class RedisCache(ICache):
    def __init__(self):
        self.redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, ttl: int):
        await self.redis.setex(key, ttl, value)

    async def delete(self, key: str):
        await self.redis.delete(key)
