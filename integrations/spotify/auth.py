import loguru
from async_spotify import SpotifyApiClient
from async_spotify.authentification import SpotifyAuthorisationToken
from async_spotify.authentification.authorization_flows import (
    AuthorizationCodeFlow,
)
from fastapi import APIRouter

from core import settings

spotify_router = APIRouter(prefix="/integrations/spotify")


auth_flow = AuthorizationCodeFlow(
    application_id=settings.SPOTIFY_CLIENT_ID,
    application_secret=settings.SPOTIFY_CLIENT_SECRET,
    scopes=settings.SPOTIFY_SCOPES,
    redirect_url=settings.SPOTIFY_REDIRECT_URL,
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
    auth_token: SpotifyAuthorisationToken = (
        await spotify_client.get_auth_token_with_code(code)
    )
    await spotify_client.create_new_client()
    return auth_token


@spotify_router.get("/playlists")
async def list_playlists():
    return await spotify_client.playlists.current_get_all()
