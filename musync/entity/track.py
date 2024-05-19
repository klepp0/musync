from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Track:
    track_id: str
    artist_id: str
    name: str
    date_added: str  # relates to playlist, requires better structure

    @classmethod
    def from_spotify(cls, track: dict) -> Track:
        return cls(
            track_id=track["track"]["id"],
            artist_id=track["track"]["artists"][0]["id"],
            name=track["track"]["name"],
            date_added=track["added_at"],
        )
