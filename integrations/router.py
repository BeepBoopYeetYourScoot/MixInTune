from fastapi import APIRouter

from core.main import app
from integrations.spotify.router import spotify_router

integrations_router = APIRouter(prefix="integrations")

integrations_router.include_router(spotify_router)
app.include_router(integrations_router)
