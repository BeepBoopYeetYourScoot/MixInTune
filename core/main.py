from fastapi import FastAPI, APIRouter

from integrations.spotify.auth import spotify_router

# from integrations.spotify.router import spotify_router
# from mixer.api.v1.router import mixer_router

app = FastAPI()
main_router = APIRouter()


@main_router.get("/")
async def homepage():
    return {"Hello": "World"}


app.include_router(spotify_router, tags=["Spotify API"])
# app.include_router(mixer_router, prefix="/v1", tags=["Mixer"])
