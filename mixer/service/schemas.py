from pydantic import BaseModel, conint

from integrations.spotify.schemas import SpotifyTrackFeatures


class CamelotWheelKey(BaseModel):
    key: int = conint(ge=1, le=11)
    mode: bool


class TuningOptions(BaseModel):
    sort_by: SpotifyTrackFeatures
    start_at_camelot_key: CamelotWheelKey
    finish_at_camelot_key: CamelotWheelKey
