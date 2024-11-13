from redis.asyncio import Redis
from typing import AsyncGenerator
from dotenv import dotenv_values
import os

# config = dotenv_values(".env")
# REDIS_URL = config['REDIS_DB_URL']
REDIS_URL =  os.getenv("REDIS_DB_URL")

async def get_redis() -> AsyncGenerator[Redis, None]:
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()
