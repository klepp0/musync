import os

import spotipy
from dotenv import load_dotenv

from musync.entity import Artist, Playlist, Track, User
from musync.session import Session

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

    @property
    def user(self) -> User:
        return User.from_spotify(self._client.me())

    def check_login(self) -> bool:
        try:
            self._client.me()
            return True
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 401:
                return False
            raise e

    def get_playlists(self) -> list[Playlist]:
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

    def get_playlist_tracks(self, playlist: Playlist) -> list[Track]:
        tracks = []
        limit = 100
        for offset in range(0, playlist.n_tracks, limit):
            spotify_tracks = self._client.playlist_tracks(
                playlist.playlist_id, limit=limit, offset=offset
            )
            tracks += [Track.from_spotify(t) for t in spotify_tracks["items"]]
            offset += limit

        return tracks

    def find_track(self, track: Track) -> Track | None:
        query = track.name
        _type = "track"

        tracks = self._client.search(query, type=_type, limit=50)["tracks"]["items"]

        for t in tracks:
            loaded_track = Track.from_spotify(t)
            if track.equals(loaded_track):
                return loaded_track
