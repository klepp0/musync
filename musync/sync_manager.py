from musync.entity import Playlist, Track
from musync.spotify import SpotifySession
from musync.tidal import TidalSession

SessionType = SpotifySession | TidalSession


class SyncManager:
    def __init__(self, session1: SessionType, session2: SessionType) -> None:
        assert isinstance(session1, (SpotifySession, TidalSession))
        assert isinstance(session2, (SpotifySession, TidalSession))
        assert session1 != session2

        self._session1 = session1
        self._session2 = session2

    def get_common_playlists(self) -> list[Playlist]:
        playlists1 = self._session1.load_playlists()
        playlists2 = self._session2.load_playlists()
        common_playlists = []
        for playlist1 in playlists1:
            for playlist2 in playlists2:
                if playlist1.name == playlist2.name:
                    common_playlists.append((playlist1, playlist2))

        return common_playlists

    def get_missing_tracks(
        self, src_playlist: Playlist, dest_playlist: Playlist
    ) -> list[Track]:
        if (
            self._session1.user.origin == dest_playlist.origin
            and self._session1.user.user_id == dest_playlist.owner_id
        ):
            src_tracks = self._session1.load_playlist_tracks(dest_playlist)
            dest_tracks = self._session2.load_playlist_tracks(src_playlist)
        elif (
            self._session2.user.user_id == dest_playlist.owner_id
            and self._session2.user.origin == dest_playlist.origin
        ):
            src_tracks = self._session2.load_playlist_tracks(dest_playlist)
            dest_tracks = self._session1.load_playlist_tracks(src_playlist)
        else:
            raise ValueError(
                "Invalid playlist"
            )  # TODO: Create more expressive custom error

        dest_track_names = [t.name for t in dest_tracks]

        return [t for t in src_tracks if t.name not in dest_track_names]
