import os

import spotipy
from dotenv import load_dotenv

from musync.entity import User
from musync.session import Session

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


class SpotifySession(Session):
    def __init__(self):
        spotify_auth = spotipy.SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="playlist-read-private",
        )
        self._client = spotipy.Spotify(auth_manager=spotify_auth)

    @property
    def user(self):
        return User.from_spotify(self._client.me())

    def check_login(self):
        try:
            self._client.me()
            return True
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 401:
                return False
            else:
                raise e
