from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.connections.redis import get_redis_connection
from core.connections.spotify import get_spotify_client


async def _on_startup():
    pass


async def _on_shutdown():
    client = await get_spotify_client(get_redis_connection())
    await client.close_client()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _on_startup()
    yield
    await _on_shutdown()
