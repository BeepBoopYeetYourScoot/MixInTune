from typing import Annotated

from fastapi import FastAPI, Depends

from core.settings import Settings, get_settings
from core.utils.lifespan import lifespan
from integrations.spotify.controllers import api_router
from integrations.spotify.sso import sso_router

settings = get_settings()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def homepage():
    return {"Hello": "World"}


@app.get("info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {"spotify_redirect_url": settings.spotify.callback_url}


app.include_router(api_router, tags=["Spotify API"])
app.include_router(sso_router, tags=["Spotify SSO"])
# app.include_router(mixer_router, prefix="/v1", tags=["Mixer"])
