from abc import ABC, abstractmethod
from typing import Iterable

import spotipy
import tidalapi

# from musync.common.entity import Playlist, Track, User
from musync.app.models import Playlist, Track, User


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
    def load_playlist(self, playlist_id: str) -> Playlist | None:
        pass

    @abstractmethod
    def load_playlists(self) -> list[Playlist]:
        pass

    @abstractmethod
    def load_playlist_tracks(self, playlist: Playlist) -> list[Track]:
        pass

    @abstractmethod
    def load_track(self, playlist_id: str) -> Track | None:
        pass

    @abstractmethod
    def find_track(self, track: Track) -> Track | None:
        pass

    @abstractmethod
    def add_to_playlist(self, playlist: Playlist, tracks: Iterable[Track]) -> Playlist:
        pass

    @abstractmethod
    def create_playlist(
        self,
        title: str,
        description: str = "This playlist was created by https://github.com/klepp0/musync 🎺",
        public: bool = False,
    ) -> Playlist:
        pass

    @abstractmethod
    def delete_playlist(self, playlist_id: str) -> Playlist:
        pass
