from pprint import pprint

from pydantic import BaseModel


class SpotifyTrack(BaseModel):
    id: str
    name: str
    artists: list
    album: dict
    duration_ms: int
    popularity: int

    @staticmethod
    def parse_from_dict(track: dict) -> "SpotifyTrack":
        pprint(track)
        return SpotifyTrack(
            id=track["id"],
            name=track["name"],
            artists=[artist["name"] for artist in track["artists"]],
            album={"name": track["album"]["name"]},
            duration_ms=track["duration_ms"],
            popularity=track["popularity"],
        )
