import tidalapi as tidal

from musync.entity import Playlist, Track
from musync.error import PlaylistNotFoundError


def load_playlist(playlist_name: str, session: tidal.Session) -> Playlist:
    for p in session.user.playlists():
        playlist = Playlist.from_tidal(p)
        if playlist.name == playlist_name:
            return playlist

    raise PlaylistNotFoundError(f"{playlist_name=}, {session.user.username=}")


def load_tracks(playlist: Playlist, session: tidal.Session) -> list[Playlist]:
    return [
        Track.from_tidal(t)
        for t in tidal.Playlist(session, playlist.playlist_id).tracks()
    ]
