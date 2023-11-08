from functools import lru_cache

from fastapi import APIRouter, Depends, Request
from fastapi_sso.sso.spotify import SpotifySSO

from core.settings import get_settings

settings = get_settings()

sso_router = APIRouter(prefix="/integrations/spotify")


@lru_cache
def get_spotify_sso():
    return SpotifySSO(
        settings.spotify.client_id,
        settings.spotify.client_secret,
        settings.spotify.callback_url,
    )


@sso_router.get("/login")
async def login(
    spotify_sso: SpotifySSO = Depends(get_spotify_sso),
):
    return await spotify_sso.get_login_redirect()


@sso_router.get("/callback")
async def authorize(
    request: Request,
    spotify_sso: SpotifySSO = Depends(get_spotify_sso),
):
    user = await spotify_sso.verify_and_process(request)
    return user
