from typing import Annotated

import loguru
from aioredis import Redis
from fastapi import APIRouter, Depends, Request
from fastapi_sso.sso.spotify import SpotifySSO

from core.connections.redis import get_redis_connection
from core.settings import get_settings

settings = get_settings()

sso_router = APIRouter(prefix="/integrations/spotify")


def get_spotify_sso():
    return SpotifySSO(
        settings.spotify.client_id,
        settings.spotify.client_secret,
        settings.spotify.callback_url,
    )


def _generate_redis_key_value_pair(
    key: str, access_token: str, refresh_token: str
):
    assert isinstance(key, str)
    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)
    access_key = f"{key}:access_token"
    refresh_key = f"{key}:refresh_token"
    return (access_key, access_token), (refresh_key, refresh_token)


@sso_router.get("/login")
async def login(
    spotify_sso: SpotifySSO = Depends(get_spotify_sso),
):
    return await spotify_sso.get_login_redirect()


@sso_router.get("/callback")
async def authorize(
    request: Request,
    spotify_sso: Annotated[SpotifySSO, Depends(get_spotify_sso)],
    redis: Annotated[Redis, Depends(get_redis_connection)],
):
    user = await spotify_sso.verify_and_process(request)
    access_pair, refresh_pair = _generate_redis_key_value_pair(
        user.id, spotify_sso.access_token, spotify_sso.refresh_token
    )
    await redis.set(*access_pair)
    await redis.set(*refresh_pair)
    loguru.logger.info(f"User {user.display_name} has logged in.")
    return user
