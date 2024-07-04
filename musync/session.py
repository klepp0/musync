from abc import ABC, abstractmethod
from typing import Iterable

import spotipy
import tidalapi

from musync.entity import Playlist, Track, User


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
    def load_playlists(self) -> list[Playlist]:
        pass

    @abstractmethod
    def load_playlist_tracks(self, playlist: Playlist) -> list[Track]:
        pass

    @abstractmethod
    def find_track(self, track: Track) -> Track | None:
        pass

    @abstractmethod
    def add_to_playlist(self, playlist: Playlist, tracks: Iterable[Track]) -> None:
        pass
