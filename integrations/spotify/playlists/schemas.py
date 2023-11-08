from pydantic import BaseModel


class PlaylistSchema(BaseModel):
    id: str
    name: str
    description: str
    tracks_url: str


class TrackSchema(BaseModel):
    pass
