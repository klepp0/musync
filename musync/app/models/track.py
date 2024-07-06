from __future__ import annotations

import datetime as dt
from typing import List, Optional

import pytz
import tidalapi
from pydantic import BaseModel

from musync.common.entity.utils import normalize_str

from .origin import Origin


class Track(BaseModel):
    track_id: str
    artist_ids: List[str]
    name: str
    duration: dt.timedelta
    date_added: Optional[dt.datetime] = None
    origin: Origin = Origin.UNKNOWN

    @classmethod
    def from_spotify(cls, track: dict) -> Track:
        if "track" in track.keys():
            track_id = "" if track["track"]["id"] is None else track["track"]["id"]
            artist_ids = (
                []
                if track["track"]["artists"] is None
                else [str(t["id"]) for t in track["track"]["artists"]]
            )
            name = "" if track["track"]["name"] is None else track["track"]["name"]
            duration = dt.timedelta(milliseconds=track["track"]["duration_ms"])
            date_added = (
                None
                if track["added_at"] is None
                else dt.datetime.strptime(
                    track["added_at"], "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=pytz.utc)
            )

            return cls(
                track_id=track_id,
                artist_ids=artist_ids,
                name=name,
                duration=duration,
                date_added=date_added,
                origin=Origin.SPOTIFY,
            )

        track_id = "" if track["id"] is None else track["id"]
        artist_ids = (
            [] if track["artists"] is None else [str(t["id"]) for t in track["artists"]]
        )
        name = "" if track["name"] is None else track["name"]
        duration = dt.timedelta(milliseconds=track["duration_ms"])
        origin = Origin.SPOTIFY

        return cls(
            track_id=track_id,
            artist_ids=artist_ids,
            name=name,
            duration=duration,
            date_added=None,
            origin=origin,
        )

    @classmethod
    def from_tidal(cls, track: tidalapi.Track) -> Track:
        track_id = "" if track.id is None else str(track.id)
        artist_ids = (
            []
            if track.artists is None
            else [str(artist.id) for artist in track.artists]
        )
        name = "" if track.name is None else track.name
        duration = (
            dt.timedelta(seconds=-1)
            if track.duration is None
            else dt.timedelta(seconds=track.duration)
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

    def equals(self, other: Track) -> bool:
        if not isinstance(other, Track):
            raise TypeError(f"Expected Track, got {type(other)}")

        tracks_are_equal = (
            normalize_str(self.name) == normalize_str(other.name)
            and abs(self.duration - other.duration).seconds < 2
        )

        if not tracks_are_equal or self.origin != other.origin:
            return tracks_are_equal

        tracks_are_equal = set(self.artist_ids) == set(other.artist_ids)

        return tracks_are_equal
