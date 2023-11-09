from typing import Annotated

import loguru
from aioredis import Redis
from async_spotify import SpotifyApiClient
from async_spotify.authentification import SpotifyAuthorisationToken
from async_spotify.authentification.authorization_flows import (
    AuthorizationCodeFlow,
)
from fastapi import APIRouter, Depends

from core.connections import get_redis_connection
from core.settings import get_settings
from integrations.spotify.schemas import SpotifyTrack, SpotifyTrackFeatures

settings = get_settings()

api_router = APIRouter(prefix="/integrations/spotify")


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


@api_router.get("/playlists")
async def list_playlists(
    spotify_client: SpotifyClient,
):
    return await spotify_client.playlists.current_get_all()


@api_router.get("/playlists/{playlist_id}/tracks")
async def list_playlist_tracks(
    playlist_id: str,
    spotify_client: SpotifyClient,
):
    return await spotify_client.playlists.get_tracks(playlist_id)


def _extract_track_objects(tracks: dict):
    return [
        SpotifyTrack.parse_from_dict(item["track"]) for item in tracks["items"]
    ]


def _extract_track_features(features: dict):
    return SpotifyTrackFeatures


@api_router.get("/playlists/{playlist_id}/features")
async def list_playlist_track_features(
    playlist_id: str,
    spotify_client: SpotifyClient,
):
    tracks = _extract_track_objects(
        await spotify_client.playlists.get_tracks(playlist_id)
    )
    return await spotify_client.track.several_audio_features(
        [track.id for track in tracks]
    )


@api_router.get("/tracks/{track_id}/analysis")
async def list_track_features(
    track_id: str,
    spotify_client: SpotifyClient,
):
    """
    Warning: Analysis may take some time
    """
    return await spotify_client.track.audio_analyze(track_id)
