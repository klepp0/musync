from __future__ import annotations

from dataclasses import dataclass

import tidalapi as tidal

from .origin import Origin


@dataclass(frozen=True, slots=True)
class User:
    user_id: str
    name: str
    origin: Origin = Origin.UNKNOWN

    @classmethod
    def from_spotify(cls, user: dict) -> User:
        return cls(
            user_id=user["id"],
            name=user["display_name"],
            origin=Origin.SPOTIFY,
        )

    @classmethod
    def from_tidal(cls, user: tidal.LoggedInUser) -> User:
        return cls(
            user_id="" if user.id is None else str(user.id),
            name="" if user.username is None else user.username,
            origin=Origin.TIDAL,
        )
