from musync.session import Session
from musync.entity import User

from pathlib import Path

import tidalapi


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
