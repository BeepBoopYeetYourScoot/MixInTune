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
        assert isinstance(track, dict)
        return SpotifyTrack(
            id=track["id"],
            name=track["name"],
            artists=[artist["name"] for artist in track["artists"]],
            album={"name": track["album"]["name"]},
            duration_ms=track["duration_ms"],
            popularity=track["popularity"],
        )


class SpotifyTrackFeatures(BaseModel):
    acousticness: float
    danceability: float
    duration_ms: int
    energy: float
    id: str
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: int  # 0/1 for minor/major
    speechiness: float
    tempo: float
    time_signature: int  # X/4; число четвертей
    valence: str

    @staticmethod
    def parse_from_dict(features: dict) -> "SpotifyTrackFeatures":
        assert isinstance(features, dict)
        return SpotifyTrackFeatures(
            acousticness=features["acousticness"],
            danceability=features["danceability"],
            duration_ms=features["duration_ms"],
            energy=features["energy"],
            id=features["id"],
            instrumentalness=features["instrumentalness"],
            key=features["key"],
            liveness=features["liveness"],
            loudness=features["loudness"],
            mode=features["mode"],
            speechiness=features["speechiness"],
            tempo=features["tempo"],
            time_signature=features["time_signature"],
            valence=features["valence"],
        )
