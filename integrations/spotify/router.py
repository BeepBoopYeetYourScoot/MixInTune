from fastapi import APIRouter

from core.main import app

spotify_router = APIRouter(prefix="spotify")

app.include_router(spotify_router)
