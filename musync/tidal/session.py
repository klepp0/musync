from pathlib import Path

import tidalapi

from musync.entity import Artist, Playlist, Track, User
from musync.session import Session

TIDAL_DIR = Path(__file__).parent.parent.parent.resolve()


class TidalSession(Session):
    _client: tidalapi.Session

    def __init__(self) -> None:
        session_file = TIDAL_DIR / "tidal-session-oauth.json"
        self._client = tidalapi.Session()
        self._client.login_session_file(session_file)

    @property
    def user(self) -> User:
        return User.from_tidal(self._client.user)

    def check_login(self) -> bool:
        return self._client.check_login()

    def load_playlists(self) -> list[Playlist]:
        return [Playlist.from_tidal(p) for p in self._client.user.playlists()]

    def load_playlist_tracks(self, playlist: Playlist) -> list[Track]:
        tidal_playlist = self._client.playlist(playlist.playlist_id)

        return [Track.from_tidal(t) for t in tidal_playlist.tracks()]

    def find_track(self, track: Track) -> Track | None:
        query = track.name

        tracks = self._client.search(query, models=[tidalapi.Track])["tracks"]

        for tr in tracks:
            loaded_track = Track.from_tidal(tr)
            if track.equals(loaded_track):
                return loaded_track

        return None

    def load_artist(self, artist_id: str) -> Artist | None:
        artist = self._client.artist(int(artist_id))
        if not isinstance(artist, tidalapi.Artist):
            return None

        return Artist.from_tidal(artist)
