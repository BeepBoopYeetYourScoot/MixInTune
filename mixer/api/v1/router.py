from fastapi import APIRouter

from integrations.spotify.router import SpotifyClient
from mixer.service.schemas import TuningOptions

mixer_router = APIRouter(prefix="/mixer")


@mixer_router.post("/playlists/{playlist_id}/sort")
async def sort_playlist(
    playlist_id: str,
    tuning_options: TuningOptions,
    spotify_client: SpotifyClient,
):
    pass
