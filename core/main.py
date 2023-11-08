from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends

from core.settings import Settings, get_settings
from integrations.spotify.auth import spotify_router, spotify_client


def _on_startup():
    pass


def _on_shutdown():
    spotify_client.close_client()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _on_startup()
    yield
    _on_shutdown()


app = FastAPI(lifespan=lifespan)
main_router = APIRouter()


@main_router.get("/")
async def homepage():
    return {"Hello": "World"}


@main_router.get("info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {"spotify_redirect_url": settings.spotify_settings.redirect_url}


app.include_router(spotify_router, tags=["Spotify API"])
# app.include_router(mixer_router, prefix="/v1", tags=["Mixer"])
