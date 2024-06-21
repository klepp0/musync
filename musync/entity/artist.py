from __future__ import annotations

from dataclasses import dataclass

import tidalapi as tidal


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

    @classmethod
    def from_tidal(cls, artist: tidal.Artist) -> Artist:
        return cls(
            artist_id="" if artist.id is None else str(artist.id),
            name="" if artist.name is None else artist.name,
        )
