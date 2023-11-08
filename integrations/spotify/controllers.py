from typing import Annotated

from async_spotify import SpotifyApiClient
from async_spotify.authentification import SpotifyAuthorisationToken
from async_spotify.authentification.authorization_flows import (
    AuthorizationCodeFlow,
)
from fastapi import APIRouter, Depends
from fastapi_sso.sso.spotify import SpotifySSO

from core.settings import get_settings
from integrations.spotify.sso import get_spotify_sso

settings = get_settings()

api_router = APIRouter(prefix="/integrations/spotify")


def get_spotify_client(sso: SpotifySSO):
    auth_flow = AuthorizationCodeFlow(
        settings.spotify.client_id,
        settings.spotify.client_secret,
        settings.spotify.scopes,
        settings.spotify.callback_url,
    )
    auth_token = SpotifyAuthorisationToken(
        access_token=sso.access_token, refresh_token=sso.refresh_token
    )
    return SpotifyApiClient(
        authorization_flow=auth_flow,
        hold_authentication=True,
        spotify_authorisation_token=auth_token,
    )


@api_router.get("/playlists")
async def list_playlists(
    sso: Annotated[SpotifySSO, Depends(get_spotify_sso)],
    spotify_client: Annotated[SpotifyApiClient, Depends(get_spotify_client)],
    response_model=None,
):
    return await spotify_client.playlists.current_get_all()


@api_router.get("/playlists/{playlist_id}/tracks")
async def list_playlist_tracks(
    playlist_id: str,
    sso: Annotated[SpotifySSO, Depends(get_spotify_sso)],
    spotify_client: Annotated[SpotifyApiClient, Depends(get_spotify_client)],
    response_model=None,
):
    return await spotify_client.playlists.get_tracks(playlist_id)


@api_router.get("/tracks/{tracks_id}/features")
async def list_track_features(
    track_id: str,
    sso: Annotated[SpotifySSO, Depends(get_spotify_sso)],
    spotify_client: Annotated[SpotifyApiClient, Depends(get_spotify_client)],
    response_model=None,
):
    return await spotify_client.track.audio_analyze(track_id)
