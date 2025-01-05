import os

import aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from api import contacts, auth, users

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379")
app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router)
app.include_router(auth.router)
app.include_router(users.router)
