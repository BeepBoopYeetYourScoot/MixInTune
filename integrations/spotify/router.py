from fastapi import APIRouter

from core.connections.spotify import SpotifyClient
from core.settings import get_settings
from integrations.spotify.schemas import (
    SpotifyTrack,
    SpotifyTrackFeatures,
)

settings = get_settings()

api_router = APIRouter(prefix="/integrations/spotify")


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
