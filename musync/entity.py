from __future__ import annotations

from dataclasses import dataclass


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
