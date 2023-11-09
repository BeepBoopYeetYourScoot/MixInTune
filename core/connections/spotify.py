from typing import Annotated

import loguru
from aioredis import Redis
from async_spotify import SpotifyApiClient
from async_spotify.authentification import SpotifyAuthorisationToken
from async_spotify.authentification.authorization_flows import (
    AuthorizationCodeFlow,
)
from fastapi import Depends

from core.connections.redis import get_redis_connection
from core.main import settings


async def get_spotify_client(
    redis: Annotated[Redis, Depends(get_redis_connection)]
) -> SpotifyApiClient:
    auth_flow = AuthorizationCodeFlow(
        settings.spotify.client_id,
        settings.spotify.client_secret,
        settings.spotify.scopes,
        settings.spotify.callback_url,
    )
    access_token = await redis.get("dovakino_o:access_token")
    refresh_token = await redis.get("dovakino_o:refresh_token")

    if isinstance(access_token, bytes):
        access_token = access_token.decode("utf-8")
    if isinstance(refresh_token, bytes):
        refresh_token = refresh_token.decode("utf-8")

    auth_token = SpotifyAuthorisationToken(
        access_token=access_token,
        refresh_token=refresh_token,
        activation_time=60000,
    )

    loguru.logger.debug(
        f"Creating Spotify client: \n"
        f"{auth_token.access_token=} \n "
        f"{auth_token.refresh_token=} \n"
        f"{auth_token.activation_time=} \n"
    )
    loguru.logger.debug(f"{auth_token.valid=}")

    client = SpotifyApiClient(
        authorization_flow=auth_flow,
        spotify_authorisation_token=auth_token,
    )
    await client.create_new_client()
    return client


# That's how FastAPI dynamic annotations work
SpotifyClient = Annotated[SpotifyApiClient, Depends(get_spotify_client)]
