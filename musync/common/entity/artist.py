from __future__ import annotations

from dataclasses import dataclass

import tidalapi as tidal

from .origin import Origin


@dataclass(frozen=True, slots=True)
class Artist:
    artist_id: str
    name: str
    origin: Origin = Origin.UNKNOWN

    @classmethod
    def from_spotify(cls, artist: dict) -> Artist:
        return cls(artist_id=artist["id"], name=artist["name"], origin=Origin.SPOTIFY)

    @classmethod
    def from_tidal(cls, artist: tidal.Artist) -> Artist:
        return cls(
            artist_id="" if artist.id is None else str(artist.id),
            name="" if artist.name is None else artist.name,
            origin=Origin.TIDAL,
        )
