from __future__ import annotations

import tidalapi
from pydantic import BaseModel

from .origin import Origin


class Playlist(BaseModel):
    playlist_id: str
    owner_id: str
    name: str
    n_tracks: int
    origin: Origin = Origin.UNKNOWN

    @classmethod
    def from_spotify(cls, playlist: dict) -> Playlist:
        return cls(
            playlist_id=playlist["id"],
            owner_id=playlist["owner"]["id"],
            name=playlist["name"],
            n_tracks=playlist["tracks"]["total"],
            origin=Origin.SPOTIFY,
        )

    @classmethod
    def from_tidal(cls, playlist: tidalapi.Playlist) -> Playlist:
        return cls(
            playlist_id="" if playlist.id is None else str(playlist.id),
            owner_id=(
                ""
                if playlist.creator is None or playlist.creator.id is None
                else str(playlist.creator.id)
            ),
            name="" if playlist.name is None else playlist.name,
            n_tracks=playlist.num_tracks,
            origin=Origin.TIDAL,
        )
