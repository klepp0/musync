import logging
from typing import Literal, Tuple

from fastapi import APIRouter, HTTPException

# from musync.common.entity import Playlist
from musync.app.models import Playlist
from musync.common.sync_manager import SyncManager
from musync.spotify import SpotifySession
from musync.tidal import TidalSession

logger = logging.getLogger("uvicorn")
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post("/sync/playlists/", response_model=Tuple[Playlist, Playlist])
def sync_playlists(
    playlist_id1: str,
    origin1: Literal["spotify", "tidal"],
    playlist_id2: str,
    origin2: Literal["spotify", "tidal"],
) -> Tuple[Playlist, Playlist]:
    match origin1, origin2:
        case "spotify", "tidal":
            session1 = SpotifySession()
            session2 = TidalSession()
        case "tidal", "spotify":
            session1 = TidalSession()
            session2 = SpotifySession()
        case "spotify", "spotify":
            session1 = SpotifySession()
            session2 = session1
        case "tidal", "tidal":
            session1 = TidalSession()
            session2 = session1
        case _:
            raise HTTPException(
                status_code=400,
                detail=f"Origin must be either 'spotify' or 'tidal' ({origin1=}, {origin2=}).",
            )

    playlist1 = session1.load_playlist(playlist_id1)
    playlist2 = session2.load_playlist(playlist_id2)

    if not playlist1 or not playlist2:
        raise HTTPException(
            status_code=404,
            detail=f"Playlist with ID {playlist_id1} or {playlist_id2} not found.",
        )

    sync_manager = SyncManager(session1, session2)

    updated_playlist2 = sync_manager.sync_playlists(playlist1, playlist2)
    updated_playlist1 = sync_manager.sync_playlists(playlist2, playlist1)

    n_added_1 = updated_playlist1.n_tracks - playlist1.n_tracks
    n_added_2 = updated_playlist2.n_tracks - playlist2.n_tracks

    logger.info(
        "Synced playlists! Added %d tracks to %s and %d tracks to %s.",
        n_added_1,
        playlist1,
        n_added_2,
        playlist2,
    )

    return updated_playlist1, updated_playlist2
