import logging
from typing import List, Literal, Optional

from fastapi import APIRouter, HTTPException

# from musync.common.entity import Playlist
from musync.app.models import Playlist, Track
from musync.spotify import SpotifySession
from musync.tidal import TidalSession

logger = logging.getLogger("uvicorn")
logging.basicConfig(level=logging.INFO)

router = APIRouter()


### GET ###
@router.get("/playlists/{origin}/{playlist_id}", response_model=Playlist)
def get_playlist(
    playlist_id: str, origin: Literal["spotify", "tidal"]
) -> Optional[Playlist]:
    match origin:
        case "spotify":
            session = SpotifySession()
        case "tidal":
            session = TidalSession()
        case _:
            raise HTTPException(
                status_code=400,
                detail=f"Origin must be either 'spotify' or 'tidal' ({origin=}).",
            )

    return session.load_playlist(playlist_id)


@router.get("/playlists/{origin}", response_model=List[Playlist])
def get_user_playlists(origin: Literal["spotify", "tidal"]) -> Optional[List[Playlist]]:
    match origin:
        case "spotify":
            session = SpotifySession()
        case "tidal":
            session = TidalSession()
        case _:
            raise HTTPException(
                status_code=400,
                detail=f"Origin must be either 'spotify' or 'tidal' ({origin=}).",
            )

    return session.load_playlists()


@router.get("/playlists/{origin}/{playlist_id}/tracks", response_model=List[Track])
def get_playlist_tracks(
    playlist_id: str, origin: Literal["spotify", "tidal"]
) -> Optional[List[Track]]:
    match origin:
        case "spotify":
            session = SpotifySession()
        case "tidal":
            session = TidalSession()
        case _:
            raise HTTPException(
                status_code=400,
                detail=f"Origin must be either 'spotify' or 'tidal' ({origin=}).",
            )

    playlist = session.load_playlist(playlist_id)
    if not playlist:
        return None

    return session.load_playlist_tracks(playlist)


### POST ###
@router.post("/playlists/{origin}/", response_model=Playlist)
def create_playlist(title: str, origin: Literal["spotify", "tidal"]) -> Playlist:
    match origin:
        case "spotify":
            session = SpotifySession()
        case "tidal":
            session = TidalSession()
        case _:
            raise HTTPException(
                status_code=400,
                detail=f"Origin must be either 'spotify' or 'tidal' ({origin=}).",
            )

    new_playlist = session.create_playlist(title)
    logger.info(f"Created playlist: {new_playlist}")

    return new_playlist


@router.post("/playlists/{origin}/{playlist_id}/tracks", response_model=Playlist)
def add_tracks_to_playlist(
    playlist_id: str,
    origin: Literal["spotify", "tidal"],
    track_ids: List[str],
) -> Playlist:
    match origin:
        case "spotify":
            session = SpotifySession()
        case "tidal":
            session = TidalSession()
        case _:
            raise HTTPException(
                status_code=400,
                detail=f"Origin must be either 'spotify' or 'tidal' ({origin=}).",
            )

    playlist = session.load_playlist(playlist_id)
    if not playlist:
        raise HTTPException(
            status_code=404,
            detail=f"Playlist with ID {playlist_id} not found.",
        )

    tracks = [session.load_track(_id) for _id in track_ids]
    updated_playlist = session.add_to_playlist(playlist, tracks)

    logger.info(f"Added {tracks=} to playlist: {updated_playlist}")

    return updated_playlist


### DELETE ###
@router.delete("/playlists/{origin}/{playlist_id}", response_model=Playlist)
def delete_playlist(
    playlist_id: str, origin: Literal["spotify", "tidal"]
) -> Optional[Playlist]:
    match origin:
        case "spotify":
            session = SpotifySession()
        case "tidal":
            session = TidalSession()
        case _:
            raise HTTPException(
                status_code=400,
                detail=f"Origin must be either 'spotify' or 'tidal' ({origin=}).",
            )

    deleted_playlist = session.delete_playlist(playlist_id)

    if not deleted_playlist:
        raise HTTPException(
            status_code=404,
            detail=f"Playlist with ID {playlist_id} not found.",
        )

    logger.info(f"Deleted playlist: {deleted_playlist}")

    return deleted_playlist
