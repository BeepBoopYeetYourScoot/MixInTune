from functools import lru_cache

import dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class SpotifySettings(BaseModel):
    client_id: str = "3a1255e198e14137b9a5f30fc6ec30a5"
    client_secret: str = "e3036089552a4ea79ca5ccf8bac45f80"
    scopes: list[str] = []
    callback_url: str = "http://localhost:8080/integrations/spotify/callback"


class Settings(BaseSettings):
    spotify: SpotifySettings = SpotifySettings()


@lru_cache
def get_settings():
    return Settings()
