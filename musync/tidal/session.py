import warnings
from typing import Iterable

import tidalapi
import tidalapi.exceptions

# from musync.common.entity import Artist, Origin, Playlist, Track, User
from musync import ROOT_DIR
from musync.app.models import Artist, Origin, Playlist, Track, User
from musync.common.error import (
    IncompatibleEntityError,
    MissingPrivilegesError,
    NotConnectedWarning,
)
from musync.common.session import Session


class TidalSession(Session):
    _client: tidalapi.Session

    def __init__(self) -> None:
        session_file = ROOT_DIR / "tidal-session-oauth.json"
        self._client = tidalapi.Session()
        self._client.login_session_file(session_file)
        if not self.check_login():
            warnings.warn("TidalSession is not connected.", NotConnectedWarning)

    @property
    def user(self) -> User:
        return User.from_tidal(self._client.user)

    def check_login(self) -> bool:
        return self._client.check_login()

    def load_playlist(self, playlist_id) -> Playlist | None:
        try:
            playlist_response = self._client.playlist(playlist_id)
            return Playlist.from_tidal(playlist_response)
        except tidalapi.exceptions.ObjectNotFound:
            return None

    def load_playlists(self) -> list[Playlist]:
        return [Playlist.from_tidal(p) for p in self._client.user.playlists()]

    def load_playlist_tracks(self, playlist: Playlist) -> list[Track]:
        tidal_playlist = self._client.playlist(playlist.playlist_id)

        return [Track.from_tidal(t) for t in tidal_playlist.tracks()]

    def load_track(self, track_id: str) -> Track:
        track = self._client.track(track_id)
        if not isinstance(track, tidalapi.Track):
            raise ValueError(f"Track with ID {track_id} not found.")

        return Track.from_tidal(track)

    def find_track(self, track: Track) -> Track | None:
        query = track.name

        tracks = self._client.search(query, models=[tidalapi.Track])["tracks"]

        for tr in tracks:
            loaded_track = Track.from_tidal(tr)
            if track.equals(loaded_track):
                return loaded_track

        return None

    def load_artist(self, artist_id: str) -> Artist | None:
        artist = self._client.artist(artist_id)
        if not isinstance(artist, tidalapi.Artist):
            return None

        return Artist.from_tidal(artist)

    def add_to_playlist(self, playlist: Playlist, tracks: Iterable[Track]) -> Playlist:
        if playlist.origin != Origin.TIDAL:
            raise IncompatibleEntityError(f"Playlist is not from Tidal ({playlist=}).")

        if not all(tr.origin == Origin.TIDAL for tr in tracks):
            raise IncompatibleEntityError(
                f"The tracks contain tracks that are not from Tidal ({tracks=})."
            )

        if self.user.user_id != playlist.owner_id:
            raise MissingPrivilegesError(
                f"The session user does not own the playlist ({playlist=})."
            )

        track_ids = [tr.track_id for tr in tracks]
        tidal_playlist = self._client.playlist(playlist.playlist_id)
        tidal_playlist.add(track_ids)

        return Playlist.from_tidal(tidal_playlist)

    def create_playlist(
        self,
        title: str,
        description: str = "This playlist was created by https://github.com/klepp0/musync 🎺",
    ) -> Playlist:
        playlist_response = self._client.user.create_playlist(
            title,
            description,
        )

        return Playlist.from_tidal(playlist_response)

    def delete_playlist(self, playlist_id: str) -> Playlist:
        tidal_playlist = self._client.playlist(playlist_id)
        tidal_playlist.delete()
        playlist = Playlist.from_tidal(tidal_playlist)

        return playlist
