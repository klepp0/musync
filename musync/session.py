from abc import ABC, abstractmethod

import spotipy
import tidalapi

from musync.entity import Playlist, User


class Session(ABC):
    _client: spotipy.Spotify | tidalapi.Session

    @property
    @abstractmethod
    def user(self) -> User:
        pass

    @abstractmethod
    def check_login(self) -> bool:
        pass

    @abstractmethod
    def get_playlists(self) -> list[Playlist]:
        pass
