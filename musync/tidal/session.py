from pathlib import Path

import tidalapi

from musync.entity import Playlist, User
from musync.session import Session


class TidalSession(Session):
    def __init__(self) -> None:
        session_file = Path("tidal-session-oath.json")
        self._client = tidalapi.Session()
        self._client.login_session_file(session_file)

    @property
    def user(self) -> User:
        return User.from_tidal(self._client.user)

    def check_login(self) -> bool:
        return self._client.check_login()

    def get_playlists(self) -> list[Playlist]:
        return [Playlist.from_tidal(p) for p in self._client.user.playlists()]
