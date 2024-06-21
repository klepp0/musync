import os

import spotipy
from dotenv import load_dotenv

from musync.entity import Playlist, Track, User
from musync.error import PlaylistNotFoundError

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


def load_playlist(playlist_name: str, user: User) -> Playlist:
    spotify_auth = spotipy.SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-read-private",
    )

    spotify_client = spotipy.Spotify(auth_manager=spotify_auth)

    limit = 50
    owned_playlists_raw = spotify_client.current_user_playlists(limit=limit, offset=0)
    owned_playlists = [
        Playlist.from_spotify(item)
        for item in owned_playlists_raw["items"]
        if item["owner"]["id"] == user.user_id
    ]
    n_playlists = owned_playlists_raw["total"]

    for offset in range(limit, n_playlists, limit):
        owned_playlists_raw = spotify_client.current_user_playlists(
            limit=limit, offset=offset
        )
        owned_playlists += [
            Playlist.from_spotify(item)
            for item in owned_playlists_raw["items"]
            if item["owner"]["id"] == user.user_id
        ]

    concrete_playlist = next(
        (p for p in owned_playlists if p.name == playlist_name), None
    )

    if concrete_playlist is None:
        raise PlaylistNotFoundError(
            f"Playlist `{playlist_name}` not found in `{user.name}'s` (user_id={user.user_id}) playlists."
        )

    return concrete_playlist


def load_tracks(playlist: Playlist) -> list[Track]:
    spotify_auth = spotipy.SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-read-private",
    )

    spotify_client = spotipy.Spotify(auth_manager=spotify_auth)

    tracks = []
    limit = 100
    for offset in range(0, playlist.n_tracks, limit):
        tracks_raw = spotify_client.playlist_tracks(
            playlist.playlist_id, limit=limit, offset=offset
        )
        tracks += [Track.from_spotify(track) for track in tracks_raw["items"]]
        offset += limit

    return tracks


def main(playlist_name: str) -> None:
    spotify_auth = spotipy.SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-read-private",
    )

    user = User.from_spotify(spotipy.Spotify(auth_manager=spotify_auth).me())
    playlist = load_playlist(playlist_name, user)
    tracks = load_tracks(playlist)

    print(tracks, len(tracks))


if __name__ == "__main__":
    main("My Shazam Tracks")
