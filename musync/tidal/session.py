from pathlib import Path

import tidalapi

from musync.entity import Origin, Playlist, Track, User
from musync.session import Session
from musync.tidal.utils import load_playlist

TIDAL_DIR = Path(__file__).parent.parent.parent.resolve()


class TidalSession(Session):
    def __init__(self) -> None:
        session_file = TIDAL_DIR / "tidal-session-oauth.json"
        self._client = tidalapi.Session()
        self._client.login_session_file(session_file)

    @property
    def user(self) -> User:
        return User.from_tidal(self._client.user)

    def check_login(self) -> bool:
        return self._client.check_login()

    def get_playlists(self) -> list[Playlist]:
        return [Playlist.from_tidal(p) for p in self._client.user.playlists()]

    def get_playlist_tracks(self, playlist: Playlist) -> list[Playlist]:
        tidal_playlist = self._client.playlist(playlist.playlist_id)

        return [Track.from_tidal(t) for t in tidal_playlist.tracks()]
