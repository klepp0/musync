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
            track_response = session._client.track(track_id)
            return Track.from_spotify(track_response)
        case "tidal":
            session = TidalSession()
            track_response = session._client.track(track_id)
            return Track.from_tidal(track_response)
        case _:
            raise ValueError(f"Origin must be either 'spotify' or 'tidal' ({origin=}).")
