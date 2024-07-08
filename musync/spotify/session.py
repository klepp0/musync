import os
import warnings
from typing import Iterable

import spotipy
from dotenv import load_dotenv

# from musync.common.entity import Artist, Origin, Playlist, Track, User
from musync.app.models import Artist, Origin, Playlist, Track, User
from musync.common.error import NotConnectedWarning
from musync.common.session import Session

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


class SpotifySession(Session):
    _client: spotipy.Spotify

    def __init__(self) -> None:
        spotify_auth = spotipy.SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="playlist-read-private",
        )
        self._client = spotipy.Spotify(auth_manager=spotify_auth)
        if not self.check_login():
            warnings.warn("SpotifySession is not connected.", NotConnectedWarning)

    @property
    def user(self) -> User:
        return User.from_spotify(self._client.me())

    def check_login(self) -> bool:
        try:
            self._client.me()
            return True
        except spotipy.exceptions.SpotifyException as exc:
            if exc.http_status == 401:
                return False
            raise exc

    def load_playlist(self, playlist_id: str) -> Playlist | None:
        try:
            playlist_response = self._client.playlist(playlist_id)
            return Playlist.from_spotify(playlist_response)
        except spotipy.exceptions.SpotifyException:
            return None

    def load_playlists(self) -> list[Playlist]:
        if not self.check_login():
            raise ConnectionError("SpotifySession is not connected.")

        limit = 50
        playlist_response = self._client.current_user_playlists(limit=limit, offset=0)
        playlists = [Playlist.from_spotify(item) for item in playlist_response["items"]]
        n_playlists = playlist_response["total"]

        for offset in range(limit, n_playlists, limit):
            playlist_response = self._client.current_user_playlists(
                limit=limit, offset=offset
            )
            playlists += [
                Playlist.from_spotify(item) for item in playlist_response["items"]
            ]

        return playlists

    def load_playlist_tracks(self, playlist: Playlist) -> list[Track]:
        tracks = []
        limit = 100
        for offset in range(0, playlist.n_tracks, limit):
            spotify_tracks = self._client.playlist_tracks(
                playlist.playlist_id, limit=limit, offset=offset
            )
            tracks += [Track.from_spotify(t) for t in spotify_tracks["items"]]
            offset += limit

        return tracks

    def load_track(self, track_id: str) -> Track:
        track = self._client.track(track_id)
        return Track.from_spotify(track)

    def find_track(self, track: Track) -> Track | None:
        query = track.name

        search_response = self._client.search(query, type="track", limit=50)
        tracks = [] if search_response is None else search_response["tracks"]["items"]

        for tr in tracks:
            loaded_track = Track.from_spotify(tr)
            if track.equals(loaded_track):
                return loaded_track

        return None

    def load_artist(self, artist_id: str) -> Artist | None:
        artist = self._client.artist(artist_id)
        if isinstance(artist, dict):
            return Artist.from_spotify(artist)

        return None

    def add_to_playlist(self, playlist: Playlist, tracks: Iterable[Track]) -> Playlist:
        if playlist.origin != Origin.SPOTIFY:
            raise ValueError(f"Playlist is not from Spotify ({playlist=}).")

        if not all(tr.origin == Origin.SPOTIFY for tr in tracks):
            raise ValueError(
                f"The tracks contain tracks that are not from Spotify ({tracks=})."
            )

        if self.user.user_id != playlist.owner_id:
            raise ValueError(
                f"The session user does not own the playlist ({playlist=})."
            )

        user_id = self.user.user_id
        playlist_id = playlist.playlist_id
        track_ids = [tr.track_id for tr in tracks]
        self._client.user_playlist_add_tracks(user_id, playlist_id, track_ids)
        client_response = self._client.playlist(playlist_id)

        return Playlist.from_spotify(client_response)

    def create_playlist(
        self,
        title: str,
        description: str = "This playlist was created by https://github.com/klepp0/musync 🎺",
    ) -> Playlist:
        playlist_response = self._client.user_playlist_create(
            self.user.user_id,
            title,
            public=False,
            description=description,
        )

        return Playlist.from_spotify(playlist_response)

    def delete_playlist(self, playlist_id: str) -> Playlist:
        playlist_response = self._client.playlist(playlist_id)
        playlist = Playlist.from_spotify(playlist_response)
        self._client.current_user_unfollow_playlist(playlist.playlist_id)

        return playlist
