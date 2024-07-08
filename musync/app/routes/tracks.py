from typing import Literal, Optional

from fastapi import APIRouter

# from musync.common.entity import Track
from musync.app.models import Track
from musync.spotify import SpotifySession
from musync.tidal import TidalSession

router = APIRouter()


@router.get("/tracks/{origin}/{track_id}", response_model=Track)
def get_track(track_id: str, origin: Literal["spotify", "tidal"]) -> Optional[Track]:
    match origin:
        case "spotify":
            session = SpotifySession()
        case "tidal":
            session = TidalSession()
        case _:
            raise ValueError(f"Origin must be either 'spotify' or 'tidal' ({origin=}).")

    return session.load_track(track_id)
