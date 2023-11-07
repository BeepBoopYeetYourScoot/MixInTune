import loguru
from async_spotify import SpotifyApiClient
from async_spotify.authentification import SpotifyAuthorisationToken
from async_spotify.authentification.authorization_flows import (
    AuthorizationCodeFlow,
)
from starlette.responses import RedirectResponse

from core import settings
from integrations.spotify.router import spotify_router

auth_flow = AuthorizationCodeFlow(
    application_id=settings.SPOTIFY_CLIENT_ID,
    application_secret=settings.SPOTIFY_CLIENT_SECRET,
    scopes=settings.SPOTIFY_SCOPES,
    redirect_url=settings.SPOTIFY_REDIRECT_URL,
)

api_client = SpotifyApiClient(auth_flow, hold_authentication=True)


@spotify_router.get("login")
async def login():
    authorization_url: str = api_client.build_authorization_url(
        show_dialog=True
    )
    loguru.logger.info(f"{authorization_url=}")
    return RedirectResponse(authorization_url, status_code=303)


@spotify_router.get("callback")
async def authorize(code: str):
    auth_token: SpotifyAuthorisationToken = (
        await api_client.get_auth_token_with_code(code)
    )
    await api_client.create_new_client()
    return auth_token
