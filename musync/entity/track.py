from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime as dt
from datetime import timedelta
from typing import Optional

import pytz
import tidalapi as tidal

from musync.entity.origin import Origin


@dataclass
class Track:
    track_id: str
    artist_ids: list[str]
    name: str
    duration: timedelta
    date_added: Optional[dt]  # relates to playlist, requires better structure
    origin: Origin = Origin.UNKNOWN

    @classmethod
    def from_spotify(cls, track: dict) -> Track:
        track_id = "" if track["track"]["id"] is None else track["track"]["id"]
        artist_ids = (
            []
            if track["track"]["artists"] is None
            else [str(t["id"]) for t in track["track"]["artists"]]
        )
        name = "" if track["track"]["name"] is None else track["track"]["name"]
        date_added = (
            None
            if track["added_at"] is None
            else dt.strptime(track["added_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=pytz.utc
            )
        )

        return cls(
            track_id=track_id,
            artist_ids=artist_ids,
            name=name,
            date_added=date_added,
            origin=Origin.SPOTIFY,
        )

    @classmethod
    def from_tidal(cls, track: tidal.Track) -> Track:
        track_id = "" if track.id is None else str(track.id)
        artist_ids = (
            []
            if track.artists is None
            else [str(artist.id) for artist in track.artists]
        )
        name = "" if track.name is None else track.name
        duration = (
            timedelta(seconds=-1)
            if track.duration is None
            else timedelta(seconds=track.duration)
        )
        date_added = (
            None
            if track.user_date_added is None
            else track.user_date_added.replace(microsecond=0)
        )

        return cls(
            track_id=track_id,
            artist_ids=artist_ids,
            name=name,
            duration=duration,
            date_added=date_added,
            origin=Origin.TIDAL,
        )
