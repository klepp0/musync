from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Artist:
    artist_id: str
    name: str

    @classmethod
    def from_spotify(cls, artist: dict) -> Artist:
        return cls(
            artist_id=artist["id"],
            name=artist["name"],
        )
