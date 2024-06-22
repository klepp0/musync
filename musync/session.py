from abc import ABC, abstractmethod
from typing import Literal

import spotipy
import tidalapi

from musync.entity import User


class Session(ABC):
    _client: Literal[spotipy.Spotify, tidalapi.Session]

    @property
    @abstractmethod
    def user(self) -> User:
        pass

    @abstractmethod
    def check_login(self) -> bool:
        pass
