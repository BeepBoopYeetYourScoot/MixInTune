import loguru
from async_spotify import SpotifyApiClient
from async_spotify.authentification import SpotifyAuthorisationToken
from async_spotify.authentification.authorization_flows import (
    AuthorizationCodeFlow,
)
from fastapi import APIRouter

from core.settings import get_settings

settings = get_settings()

spotify_router = APIRouter(prefix="/integrations/spotify")


auth_flow = AuthorizationCodeFlow(
    application_id=settings.spotify_settings.client_id,
    application_secret=settings.spotify_settings.client_secret,
    scopes=settings.spotify_settings.scopes,
    redirect_url=settings.spotify_settings.redirect_url,
)

spotify_client = SpotifyApiClient(auth_flow, hold_authentication=True)


@spotify_router.get("/login")
async def login():
    authorization_url: str = spotify_client.build_authorization_url(
        show_dialog=True
    )
    loguru.logger.info(f"{authorization_url=}")
    return authorization_url


@spotify_router.get("/callback")
async def authorize(code: str):
    # TODO Need to cache it with Redis
    auth_token: SpotifyAuthorisationToken = (
        await spotify_client.get_auth_token_with_code(code)
    )
    await spotify_client.create_new_client()
    return auth_token


@spotify_router.get("/playlists")
async def list_playlists():
    return await spotify_client.playlists.current_get_all()
