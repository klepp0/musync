from __future__ import annotations

from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    name: str

    @classmethod
    def from_spotify(cls, user: dict) -> User:
        return cls(
            user_id=user["id"],
            name=user["display_name"],
        )
