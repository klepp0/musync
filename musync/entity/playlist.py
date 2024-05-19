from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Playlist:
    playlist_id: str
    owner_id: str
    name: str
    n_tracks: int

    @classmethod
    def from_spotify(cls, playlist: dict) -> Playlist:
        return cls(
            playlist_id=playlist["id"],
            owner_id=playlist["owner"]["id"],
            name=playlist["name"],
            n_tracks=playlist["tracks"]["total"],
        )
