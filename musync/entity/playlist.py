from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Playlist:
    playlist_id: str
    name: str
    owner: str

    @classmethod
    def from_spotify(cls, playlist: dict) -> Playlist:
        return cls(
            playlist_id=playlist["id"],
            name=playlist["name"],
            owner=playlist["owner"]["id"],
        )
