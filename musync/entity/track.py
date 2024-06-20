from __future__ import annotations

from dataclasses import dataclass

import tidalapi as tidal


@dataclass
class Track:
    track_id: str
    artist_id: str
    name: str
    date_added: Optional[str]  # relates to playlist, requires better structure

    @classmethod
    def from_spotify(cls, track: dict) -> Track:
        return cls(
            track_id=track["track"]["id"],
            artist_id=track["track"]["artists"][0]["id"],
            name=track["track"]["name"],
            date_added=track["added_at"],
        )

    @classmethod
    def from_tidal(cls, track: tidal.Track) -> Track:
        return cls(
            track_id="" if track.id is None else str(track.id),
            artist_id=(
                ""
                if track.artist is None or track.artist.id is None
                else str(track.artist.id)
            ),
            name="" if track.name is None else track.name,
            date_added=(
                "" if track.user_date_added is None else str(track.user_date_added)
            ),
        )
