from __future__ import annotations

import os
from dataclasses import dataclass

import spotipy
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


@dataclass
class User:
    user_id: str
    name: str

    @classmethod
    def from_spotify(cls, user: dict) -> User:
        return User(
            user_id=user["id"],
            name=user["display_name"],
        )


@dataclass
class Playlist:
    playlist_id: str
    name: str
    owner: str

    @classmethod
    def from_spotify(cls, playlist: dict) -> Playlist:
        return Playlist(
            playlist_id=playlist["id"],
            name=playlist["name"],
            owner=playlist["owner"]["id"],
        )


@dataclass
class Track:
    track_id: str
    artist_id: str
    name: str
    date_added: str  # relates to playlist, requires better structure

    @classmethod
    def from_spotify(cls, track: dict) -> Track:
        return Track(
            track_id=track["track"]["id"],
            name=track["track"]["name"],
            artist_id=track["track"]["artists"][0]["id"],
            date_added=track["added_at"],
        )


@dataclass
class Artist:
    artist_id: str
    name: str

    @classmethod
    def from_spotify(cls, artist: dict) -> Artist:
        return Artist(
            artist_id=artist["id"],
            name=artist["name"],
        )


def load_playlist(playlist_name: str, user: User) -> Playlist:
    spotify_auth = spotipy.SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-read-private",
    )

    spotify_client = spotipy.Spotify(auth_manager=spotify_auth)

    owned_playlists_raw = spotify_client.current_user_playlists()
    owned_playlists = [
        Playlist.from_spotify(item)
        for item in owned_playlists_raw["items"]
        if item["owner"]["id"] == user.user_id
    ]
    concrete_playlist = next(
        (p for p in owned_playlists if p.name == playlist_name), None
    )

    return concrete_playlist


def load_tracks(playlist: Playlist) -> list[Tracks]:
    spotify_auth = spotipy.SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-read-private",
    )

    spotify_client = spotipy.Spotify(auth_manager=spotify_auth)

    tracks = []
    offset = 0
    limit = 100
    tracks_remaining = True
    while tracks_remaining:
        tracks_raw = spotify_client.playlist_tracks(
            playlist.playlist_id, limit=limit, offset=offset
        )
        tracks += [Track.from_spotify(track) for track in tracks_raw["items"]]
        tracks_total = tracks_raw["total"]
        offset += limit
        tracks_remaining = tracks_total > offset

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
