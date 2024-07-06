from __future__ import annotations

import tidalapi
from pydantic import BaseModel

from musync.common.entity.origin import Origin


class Artist(BaseModel):
    artist_id: str
    name: str
    origin: Origin = Origin.UNKNOWN

    @classmethod
    def from_spotify(cls, artist: dict) -> Artist:
        return cls(artist_id=artist["id"], name=artist["name"], origin=Origin.SPOTIFY)

    @classmethod
    def from_tidal(cls, artist: tidalapi.Artist) -> Artist:
        return cls(
            artist_id="" if artist.id is None else str(artist.id),
            name="" if artist.name is None else artist.name,
            origin=Origin.TIDAL,
        )
