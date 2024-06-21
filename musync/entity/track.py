from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime as dt
from typing import Optional
import pytz

import tidalapi as tidal


@dataclass
class Track:
    track_id: str
    artist_id: str
    name: str
    date_added: Optional[dt]  # relates to playlist, requires better structure

    @classmethod
    def from_spotify(cls, track: dict) -> Track:
        return cls(
            track_id=track["track"]["id"],
            artist_id=track["track"]["artists"][0]["id"],
            name=track["track"]["name"],
            date_added=(
                None
                if track["added_at"] is None
                else dt.strptime(track["added_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
            ),
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
                None if track.user_date_added is None else track.user_date_added.replace(microsecond=0)
            ),
        )
