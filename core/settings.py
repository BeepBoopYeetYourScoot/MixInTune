import dotenv

dotenv.load_dotenv()


SPOTIFY_CLIENT_ID = "3a1255e198e14137b9a5f30fc6ec30a5"
SPOTIFY_CLIENT_SECRET = "e3036089552a4ea79ca5ccf8bac45f80"
SPOTIFY_SCOPES: list[str] = []
SPOTIFY_REDIRECT_URL = "http://localhost:8080/integrations/spotify/callback"
