from __future__ import annotations

from dataclasses import dataclass

import tidalapi as tidal

from musync.entity import Origin


@dataclass
class User:
    user_id: str
    name: str
    origin: Origin = Origin.unknown

    @classmethod
    def from_spotify(cls, user: dict) -> User:
        return cls(
            user_id=user["id"],
            name=user["display_name"],
            origin=Origin.spotify,
        )

    @classmethod
    def from_tidal(cls, user: tidal.LoggedInUser) -> User:
        return cls(
            user_id="" if user.id is None else str(user.id),
            name="" if user.username is None else user.username,
            origin=Origin.tidal,
        )
