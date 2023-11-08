from contextlib import asynccontextmanager

from fastapi import FastAPI

from integrations.spotify.controllers import get_spotify_client
from integrations.spotify.sso import get_spotify_sso


async def _on_startup():
    pass


async def _on_shutdown():
    await get_spotify_client(get_spotify_sso()).close_client()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _on_startup()
    yield
    await _on_shutdown()
